from typing import TYPE_CHECKING

from sqlalchemy import exists, select

from ..model import BannedUser
from . import Repository

if TYPE_CHECKING:
    from ... import BaseAsyncDatabase


class BannedUserRepository(Repository[BannedUser]):

    def __init__(self, database: BaseAsyncDatabase) -> None:
        self._model = BannedUser
        super().__init__(database, self._model)

    async def is_exists(self, guild_id: int) -> bool:
        async with self.database.enter_session() as session:
            stmt = select(exists().where(self.get_model_cls().user_id == guild_id))
            result = await session.execute(stmt)
            is_exist = result.scalar()
            return is_exist or False
