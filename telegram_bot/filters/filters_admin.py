from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMIN


class NotAdmin(BoundFilter):
    """Фильтр для не администратора."""

    async def check(self, message: types.Message):
        return message.from_user.id != ADMIN


class IsAdmin(BoundFilter):
    """Фильтр для администратора."""

    async def check(self, message: types.Message):
        return message.from_user.id == ADMIN
