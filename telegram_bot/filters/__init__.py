from aiogram import Dispatcher

from .filters_admin import NotAdmin, IsAdmin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(NotAdmin)
    dp.filters_factory.bind(IsAdmin)
