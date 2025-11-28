from aiosqlite import Cursor, IntegrityError

from domain.exceptions import UserAlreadyExists
from domain.models import User
from domain.ports import UserRepo
from infra.repo.sqlite.base import SqliteBaseRepo
from infra.repo.sqlite.mapping import user_from_row, user_to_row


class SqliteUserRepo(SqliteBaseRepo, UserRepo):
    async def get(self, id: int):
        query = "SELECT * FROM users WHERE id = ?"
        async with self._transaction() as conn:
            cursor = await conn.execute(query, [id])
            user = await cursor.fetchone()

            return user_from_row(user) if user else None

    async def add(self, user: User):
        query = "INSERT INTO users (id, name) VALUES (:id, :name) RETURNING *"
        async with self._transaction() as conn:
            try:
                cursor: Cursor = await conn.execute(query, user_to_row(user))
                row = await cursor.fetchone()
                return user_from_row(row)
            except IntegrityError as e:
                raise UserAlreadyExists(
                    "Пользователь с таким именем уже существует!", e
                )
