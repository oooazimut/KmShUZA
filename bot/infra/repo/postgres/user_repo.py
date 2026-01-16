from psycopg.errors import UniqueViolation
from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool
from domain.entities import User
from domain.exceptions import UserAlreadyExists
from domain.ports import UserRepo

from .base_repo import PGBaseRepo
from ..mapping import user_to_row


class PGUserRepo(PGBaseRepo, UserRepo):
    def __init__(self, pool: AsyncConnectionPool) -> None:
        super().__init__(pool)
        self.row_factory = class_row(User)

    async def add(self, user: User):
        stmt = """
        INSERT INTO users (name, password, telegram_id)
        VALUES (%(name)s, %(password)s, %(telegram_id)s)
        RETURNING name, password, telegram_id
        """
        try:
            return await self._fetchone(stmt, user_to_row(user))
        except UniqueViolation:
            raise UserAlreadyExists

    async def get(self, id: int):
        stmt = "SELECT name, password, telegram_id FROM users WHERE id = %s"
        return await self._fetchone(stmt, [id])

    async def get_by_login(self, login: str):
        stmt = "SELECT name, password, telegram_id FROM users WHERE name = %s"
        return await self._fetchone(stmt, [login])

    async def get_by_tg_id(self, tg_id: int):
        stmt = "select name, password, telegram_id from users where telegram_id = %s"
        return await self._fetchone(stmt, [tg_id])

    async def remove_by_login(self, login: str):
        stmt = "DELETE FROM users WHERE name = %s"
        await self._execute(stmt, [login])
