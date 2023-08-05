# mautrix-signal - A Matrix-Signal puppeting bridge
# Copyright (C) 2021 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, AsyncIterable, Awaitable, cast
from uuid import UUID
import asyncio
import hashlib
import os.path

from yarl import URL

from mausignald.types import Address, Profile
from mautrix.appservice import IntentAPI
from mautrix.bridge import BasePuppet, async_getter_lock
from mautrix.errors import MForbidden
from mautrix.types import (
    ContentURI,
    EventType,
    PowerLevelStateEventContent,
    RoomID,
    SyncToken,
    UserID,
)
from mautrix.util.simple_template import SimpleTemplate

from . import portal as p, user as u
from .config import Config
from .db import Puppet as DBPuppet

if TYPE_CHECKING:
    from .__main__ import SignalBridge

try:
    import phonenumbers
except ImportError:
    phonenumbers = None


class Puppet(DBPuppet, BasePuppet):
    by_uuid: dict[UUID, Puppet] = {}
    by_number: dict[str, Puppet] = {}
    by_custom_mxid: dict[UserID, Puppet] = {}
    hs_domain: str
    mxid_template: SimpleTemplate[str]

    config: Config

    default_mxid_intent: IntentAPI
    default_mxid: UserID

    _uuid_lock: asyncio.Lock
    _update_info_lock: asyncio.Lock

    def __init__(
        self,
        uuid: UUID | None,
        number: str | None,
        name: str | None = None,
        name_quality: int = 0,
        avatar_url: ContentURI | None = None,
        avatar_hash: str | None = None,
        name_set: bool = False,
        avatar_set: bool = False,
        uuid_registered: bool = False,
        number_registered: bool = False,
        custom_mxid: UserID | None = None,
        access_token: str | None = None,
        next_batch: SyncToken | None = None,
        base_url: URL | None = None,
    ) -> None:
        super().__init__(
            uuid=uuid,
            number=number,
            name=name,
            name_quality=name_quality,
            avatar_url=avatar_url,
            avatar_hash=avatar_hash,
            name_set=name_set,
            avatar_set=avatar_set,
            uuid_registered=uuid_registered,
            number_registered=number_registered,
            custom_mxid=custom_mxid,
            access_token=access_token,
            next_batch=next_batch,
            base_url=base_url,
        )
        self.log = self.log.getChild(str(uuid) if uuid else number)

        self.default_mxid = self.get_mxid_from_id(self.address)
        self.default_mxid_intent = self.az.intent.user(self.default_mxid)
        self.intent = self._fresh_intent()

        self._uuid_lock = asyncio.Lock()
        self._update_info_lock = asyncio.Lock()

    @classmethod
    def init_cls(cls, bridge: "SignalBridge") -> AsyncIterable[Awaitable[None]]:
        cls.config = bridge.config
        cls.loop = bridge.loop
        cls.mx = bridge.matrix
        cls.az = bridge.az
        cls.hs_domain = cls.config["homeserver.domain"]
        cls.mxid_template = SimpleTemplate(
            cls.config["bridge.username_template"],
            "userid",
            prefix="@",
            suffix=f":{cls.hs_domain}",
            type=str,
        )
        cls.sync_with_custom_puppets = cls.config["bridge.sync_with_custom_puppets"]

        cls.homeserver_url_map = {
            server: URL(url)
            for server, url in cls.config["bridge.double_puppet_server_map"].items()
        }
        cls.allow_discover_url = cls.config["bridge.double_puppet_allow_discovery"]
        cls.login_shared_secret_map = {
            server: secret.encode("utf-8")
            for server, secret in cls.config["bridge.login_shared_secret_map"].items()
        }
        cls.login_device_name = "Signal Bridge"
        return (puppet.try_start() async for puppet in cls.all_with_custom_mxid())

    def intent_for(self, portal: p.Portal) -> IntentAPI:
        if portal.chat_id == self.address:
            return self.default_mxid_intent
        return self.intent

    @property
    def is_registered(self) -> bool:
        return self.uuid_registered if self.uuid is not None else self.number_registered

    @is_registered.setter
    def is_registered(self, value: bool) -> None:
        if self.uuid is not None:
            self.uuid_registered = value
        else:
            self.number_registered = value

    @property
    def address(self) -> Address:
        return Address(uuid=self.uuid, number=self.number)

    async def handle_uuid_receive(self, uuid: UUID) -> None:
        async with self._uuid_lock:
            if self.uuid:
                # Received UUID was handled while this call was waiting
                return
            await self._handle_uuid_receive(uuid)

    async def handle_number_receive(self, number: str) -> None:
        async with self._uuid_lock:
            if self.number == number:
                return
            if self.number:
                self.by_number.pop(self.number, None)
            self.number = number
            self.by_number[self.number] = self
            await self._set_number(number)
            async for portal in p.Portal.find_private_chats_with(Address(number=number)):
                self.log.trace(f"Updating chat_id of private chat portal {portal.receiver}")
                portal.handle_uuid_receive(self.uuid)
            prev_mxid = self.get_mxid_from_id(Address(number=number))
            if await self.az.state_store.is_registered(prev_mxid):
                prev_intent = self.az.intent.user(prev_mxid)
                await self._migrate_memberships(prev_intent, self.default_mxid_intent)

    async def _handle_uuid_receive(self, uuid: UUID) -> None:
        self.log.debug(f"Found UUID for user: {uuid}")
        user = await u.User.get_by_username(self.number)
        if user and not user.uuid:
            user.uuid = self.uuid
            user.by_uuid[user.uuid] = user
            await user.update()
        self.uuid = uuid
        self.by_uuid[self.uuid] = self
        await self._set_uuid(uuid)
        async for portal in p.Portal.find_private_chats_with(Address(number=self.number)):
            self.log.trace(f"Updating chat_id of private chat portal {portal.receiver}")
            portal.handle_uuid_receive(self.uuid)
        prev_intent = self.default_mxid_intent
        self.default_mxid = self.get_mxid_from_id(self.address)
        self.default_mxid_intent = self.az.intent.user(self.default_mxid)
        self.intent = self._fresh_intent()
        await self.default_mxid_intent.ensure_registered()
        if self.name:
            await self.default_mxid_intent.set_displayname(self.name)
        self.log = Puppet.log.getChild(str(uuid))
        await self._migrate_memberships(prev_intent, self.default_mxid_intent)

    async def _migrate_memberships(self, prev_intent: IntentAPI, new_intent: IntentAPI) -> None:
        self.log.debug(f"Migrating memberships {prev_intent.mxid} -> {new_intent.mxid}")
        try:
            joined_rooms = await prev_intent.get_joined_rooms()
        except MForbidden as e:
            self.log.debug(
                f"Got MForbidden ({e.message}) when getting joined rooms of old mxid, "
                "assuming there are no rooms to rejoin"
            )
            return
        for room_id in joined_rooms:
            await prev_intent.invite_user(room_id, self.default_mxid)
            await self._migrate_powers(prev_intent, new_intent, room_id)
            await prev_intent.leave_room(room_id)
            await new_intent.join_room_by_id(room_id)

    async def _migrate_powers(
        self, prev_intent: IntentAPI, new_intent: IntentAPI, room_id: RoomID
    ) -> None:
        try:
            powers: PowerLevelStateEventContent
            powers = await prev_intent.get_state_event(room_id, EventType.ROOM_POWER_LEVELS)
            user_level = powers.get_user_level(prev_intent.mxid)
            pl_state_level = powers.get_event_level(EventType.ROOM_POWER_LEVELS)
            if user_level >= pl_state_level > powers.users_default:
                powers.ensure_user_level(new_intent.mxid, user_level)
                await prev_intent.send_state_event(room_id, EventType.ROOM_POWER_LEVELS, powers)
        except Exception:
            self.log.warning("Failed to migrate power levels", exc_info=True)

    async def update_info(self, info: Profile | Address, source: u.User) -> None:
        update = False
        address = info.address if isinstance(info, Profile) else info
        if address.uuid and not self.uuid:
            await self.handle_uuid_receive(address.uuid)
        if address.number and address.number != self.number:
            await self.handle_number_receive(address.number)
            update = True
        self.log.debug("Updating info with %s (source: %s)", info, source.mxid)
        async with self._update_info_lock:
            if isinstance(info, Profile) or self.name is None:
                update = await self._update_name(info) or update
            if isinstance(info, Profile):
                update = await self._update_avatar(info.avatar) or update
            elif self.config["bridge.contact_list_names"] != "disallow" and self.number:
                # Try to use a contact list avatar
                update = await self._update_avatar(f"contact-{self.number}") or update
            if update:
                await self.update()
                asyncio.create_task(self._update_portal_meta())

    @staticmethod
    def fmt_phone(number: str) -> str:
        if phonenumbers is None:
            return number
        parsed = phonenumbers.parse(number)
        fmt = phonenumbers.PhoneNumberFormat.INTERNATIONAL
        return phonenumbers.format_number(parsed, fmt)

    @classmethod
    def _get_displayname(cls, info: Profile | Address) -> tuple[str, int]:
        quality = 10
        if isinstance(info, Profile):
            address = info.address
            name = None
            contact_names = cls.config["bridge.contact_list_names"]
            if info.profile_name:
                name = info.profile_name
                quality = 90 if contact_names == "prefer" else 100
            if info.contact_name:
                if contact_names == "prefer":
                    quality = 100
                    name = info.contact_name
                elif contact_names == "allow" and not name:
                    quality = 50
                    name = info.contact_name
            names = name.split("\x00") if name else []
        else:
            address = info
            names = []
        data = {
            "first_name": names[0] if len(names) > 0 else "",
            "last_name": names[-1] if len(names) > 1 else "",
            "full_name": " ".join(names),
            "phone": cls.fmt_phone(address.number) if address.number else None,
            "uuid": str(address.uuid) if address.uuid else None,
            "displayname": "Unknown user",
        }
        for pref in cls.config["bridge.displayname_preference"]:
            value = data.get(pref.replace(" ", "_"))
            if value:
                data["displayname"] = value
                break

        return cls.config["bridge.displayname_template"].format(**data), quality

    async def _update_name(self, info: Profile | Address) -> bool:
        name, quality = self._get_displayname(info)
        if quality >= self.name_quality and (name != self.name or not self.name_set):
            self.log.debug(
                "Updating name from '%s' to '%s' (quality: %d)", self.name, name, quality
            )
            self.name = name
            self.name_quality = quality
            try:
                await self.default_mxid_intent.set_displayname(self.name)
                self.name_set = True
            except Exception:
                self.log.exception("Error setting displayname")
                self.name_set = False
            return True
        elif name != self.name or not self.name_set:
            self.log.debug(
                "Not updating name from '%s' to '%s', new quality (%d) is lower than old (%d)",
                self.name,
                name,
                quality,
                self.name_quality,
            )
        elif self.name_quality == 0:
            # Name matches, but quality is not stored in database - store it now
            self.name_quality = quality
            return True
        return False

    @staticmethod
    async def upload_avatar(
        self: Puppet | p.Portal, path: str, intent: IntentAPI
    ) -> bool | tuple[str, ContentURI]:
        if not path:
            return False
        if not path.startswith("/"):
            path = os.path.join(self.config["signal.avatar_dir"], path)
        try:
            with open(path, "rb") as file:
                data = file.read()
        except FileNotFoundError:
            return False
        if not data:
            return False
        new_hash = hashlib.sha256(data).hexdigest()
        if self.avatar_set and new_hash == self.avatar_hash:
            return False
        mxc = await intent.upload_media(data, async_upload=self.config["homeserver.async_media"])
        return new_hash, mxc

    async def _update_avatar(self, path: str) -> bool:
        res = await Puppet.upload_avatar(self, path, self.default_mxid_intent)
        if res is False:
            return False
        self.avatar_hash, self.avatar_url = res
        try:
            await self.default_mxid_intent.set_avatar_url(self.avatar_url)
            self.avatar_set = True
        except Exception:
            self.log.exception("Error setting avatar")
            self.avatar_set = False
        return True

    async def _update_portal_meta(self) -> None:
        async for portal in p.Portal.find_private_chats_with(self.address):
            if portal.receiver == self.number:
                # This is a note to self chat, don't change the name
                continue
            try:
                await portal.update_puppet_name(self.name)
                await portal.update_puppet_avatar(self.avatar_hash, self.avatar_url)
                if self.number:
                    await portal.update_puppet_number(self.fmt_phone(self.number))
            except Exception:
                self.log.exception(f"Error updating portal meta for {portal.receiver}")

    async def default_puppet_should_leave_room(self, room_id: RoomID) -> bool:
        portal: p.Portal = await p.Portal.get_by_mxid(room_id)
        if not portal or not portal.is_direct:
            return True
        elif portal.chat_id.uuid and self.uuid:
            return portal.chat_id.uuid != self.uuid
        elif portal.chat_id.number and self.number:
            return portal.chat_id.number != self.number
        else:
            return True

    # region Database getters

    def _add_to_cache(self) -> None:
        if self.uuid:
            self.by_uuid[self.uuid] = self
        if self.number:
            self.by_number[self.number] = self
        if self.custom_mxid:
            self.by_custom_mxid[self.custom_mxid] = self

    async def save(self) -> None:
        await self.update()

    @classmethod
    async def get_by_mxid(cls, mxid: UserID, create: bool = True) -> Puppet | None:
        address = cls.get_id_from_mxid(mxid)
        if not address:
            return None
        return await cls.get_by_address(address, create)

    @classmethod
    @async_getter_lock
    async def get_by_custom_mxid(cls, mxid: UserID) -> Puppet | None:
        try:
            return cls.by_custom_mxid[mxid]
        except KeyError:
            pass

        puppet = cast(cls, await super().get_by_custom_mxid(mxid))
        if puppet:
            puppet._add_to_cache()
            return puppet

        return None

    @classmethod
    def get_id_from_mxid(cls, mxid: UserID) -> Address | None:
        identifier = cls.mxid_template.parse(mxid)
        if not identifier:
            return None
        if identifier.startswith("phone_"):
            return Address(number="+" + identifier[len("phone_") :])
        else:
            try:
                return Address(uuid=UUID(identifier.upper()))
            except ValueError:
                return None

    @classmethod
    def get_mxid_from_id(cls, address: Address) -> UserID:
        if address.uuid:
            identifier = str(address.uuid).lower()
        elif address.number:
            identifier = f"phone_{address.number.lstrip('+')}"
        else:
            raise ValueError("Empty address")
        return UserID(cls.mxid_template.format_full(identifier))

    @classmethod
    @async_getter_lock
    async def get_by_address(cls, address: Address, create: bool = True) -> Puppet | None:
        puppet = await cls._get_by_address(address, create)
        if puppet and address.uuid and not puppet.uuid:
            # We found a UUID for this user, store it ASAP
            await puppet.handle_uuid_receive(address.uuid)
        return puppet

    @classmethod
    async def _get_by_address(cls, address: Address, create: bool = True) -> Puppet | None:
        if not address.is_valid:
            raise ValueError("Empty address")
        if address.uuid:
            try:
                return cls.by_uuid[address.uuid]
            except KeyError:
                pass
        if address.number:
            try:
                return cls.by_number[address.number]
            except KeyError:
                pass

        puppet = cast(cls, await super().get_by_address(address))
        if puppet is not None:
            puppet._add_to_cache()
            return puppet

        if create:
            puppet = cls(address.uuid, address.number)
            await puppet.insert()
            puppet._add_to_cache()
            return puppet

        return None

    @classmethod
    async def all_with_custom_mxid(cls) -> AsyncGenerator[Puppet, None]:
        puppets = await super().all_with_custom_mxid()
        puppet: cls
        for index, puppet in enumerate(puppets):
            try:
                yield cls.by_uuid[puppet.uuid]
            except KeyError:
                try:
                    yield cls.by_number[puppet.number]
                except KeyError:
                    puppet._add_to_cache()
                    yield puppet

    # endregion
