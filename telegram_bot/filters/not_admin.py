from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import ADMIN


class NotAdmin(BoundFilter):
    '''Фильтр для проверки отправлено ли сообщение администратором или нет'''
    async def check(self, message: types.Message):
        # return message.from_user.id != ADMIN
        return message.from_user.id != 123
