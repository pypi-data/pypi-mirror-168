# mautrix-signal - A Matrix-Signal puppeting bridge
# Copyright (C) 2020 Tulir Asokan
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

from typing import TYPE_CHECKING, ClassVar
from uuid import UUID

from attr import dataclass
from yarl import URL
import asyncpg

from mausignald.types import Address
from mautrix.types import ContentURI, SyncToken, UserID
from mautrix.util.async_db import Connection, Database

fake_db = Database.create("") if TYPE_CHECKING else None


@dataclass
class Puppet:
    db: ClassVar[Database] = fake_db

    uuid: UUID | None
    number: str | None
    name: str | None
    name_quality: int
    avatar_hash: str | None
    avatar_url: ContentURI | None
    name_set: bool
    avatar_set: bool

    uuid_registered: bool
    number_registered: bool

    custom_mxid: UserID | None
    access_token: str | None
    next_batch: SyncToken | None
    base_url: URL | None

    @property
    def _base_url_str(self) -> str | None:
        return str(self.base_url) if self.base_url else None

    async def insert(self) -> None:
        q = """
        INSERT INTO puppet (uuid, number, name, name_quality, avatar_hash, avatar_url, name_set,
                            avatar_set, uuid_registered, number_registered,
                            custom_mxid, access_token, next_batch, base_url)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
        """
        await self.db.execute(
            q,
            self.uuid,
            self.number,
            self.name,
            self.name_quality,
            self.avatar_hash,
            self.avatar_url,
            self.name_set,
            self.avatar_set,
            self.uuid_registered,
            self.number_registered,
            self.custom_mxid,
            self.access_token,
            self.next_batch,
            self._base_url_str,
        )

    async def _set_uuid(self, uuid: UUID) -> None:
        async with self.db.acquire() as conn, conn.transaction():
            await conn.execute(
                "DELETE FROM puppet WHERE uuid=$1 AND number<>$2", uuid, self.number
            )
            await conn.execute("UPDATE puppet SET uuid=$1 WHERE number=$2", uuid, self.number)
            await self._update_number_to_uuid(conn, self.number, str(uuid))

    async def _set_number(self, number: str) -> None:
        async with self.db.acquire() as conn, conn.transaction():
            await conn.execute(
                "DELETE FROM puppet WHERE number=$1 AND uuid<>$2", number, self.uuid
            )
            await conn.execute("UPDATE puppet SET number=$1 WHERE uuid=$2", number, self.uuid)
            await self._update_number_to_uuid(conn, number, str(self.uuid))

    @staticmethod
    async def _update_number_to_uuid(conn: Connection, old_number: str, new_uuid: str) -> None:
        try:
            async with conn.transaction():
                await conn.execute(
                    "UPDATE portal SET chat_id=$1 WHERE chat_id=$2", new_uuid, old_number
                )
        except asyncpg.UniqueViolationError:
            await conn.execute("DELETE FROM portal WHERE chat_id=$1", old_number)
        await conn.execute("UPDATE message SET sender=$1 WHERE sender=$2", new_uuid, old_number)
        await conn.execute("UPDATE reaction SET author=$1 WHERE author=$2", new_uuid, old_number)

    async def update(self) -> None:
        set_columns = (
            "name=$3, name_quality=$4, avatar_hash=$5, avatar_url=$6, name_set=$7, avatar_set=$8, "
            "uuid_registered=$9, number_registered=$10, "
            "custom_mxid=$11, access_token=$12, next_batch=$13, base_url=$14"
        )
        q = (
            f"UPDATE puppet SET uuid=$1, {set_columns} WHERE number=$2"
            if self.uuid is None
            else f"UPDATE puppet SET number=$2, {set_columns} WHERE uuid=$1"
        )
        await self.db.execute(
            q,
            self.uuid,
            self.number,
            self.name,
            self.name_quality,
            self.avatar_hash,
            self.avatar_url,
            self.name_set,
            self.avatar_set,
            self.uuid_registered,
            self.number_registered,
            self.custom_mxid,
            self.access_token,
            self.next_batch,
            self._base_url_str,
        )

    @classmethod
    def _from_row(cls, row: asyncpg.Record) -> Puppet:
        data = {**row}
        base_url_str = data.pop("base_url")
        base_url = URL(base_url_str) if base_url_str is not None else None
        return cls(base_url=base_url, **data)

    _select_base = (
        "SELECT uuid, number, name, name_quality, avatar_hash, avatar_url, name_set, avatar_set, "
        "       uuid_registered, number_registered, custom_mxid, access_token, "
        "       next_batch, base_url "
        "FROM puppet"
    )

    @classmethod
    async def get_by_address(cls, address: Address) -> Puppet | None:
        if address.uuid:
            if address.number:
                row = await cls.db.fetchrow(
                    f"{cls._select_base} WHERE uuid=$1 OR number=$2", address.uuid, address.number
                )
            else:
                row = await cls.db.fetchrow(f"{cls._select_base} WHERE uuid=$1", address.uuid)
        elif address.number:
            row = await cls.db.fetchrow(f"{cls._select_base} WHERE number=$1", address.number)
        else:
            raise ValueError("Invalid address")
        if not row:
            return None
        return cls._from_row(row)

    @classmethod
    async def get_by_custom_mxid(cls, mxid: UserID) -> Puppet | None:
        row = await cls.db.fetchrow(f"{cls._select_base} WHERE custom_mxid=$1", mxid)
        if not row:
            return None
        return cls._from_row(row)

    @classmethod
    async def all_with_custom_mxid(cls) -> list[Puppet]:
        rows = await cls.db.fetch(f"{cls._select_base} WHERE custom_mxid IS NOT NULL")
        return [cls._from_row(row) for row in rows]
