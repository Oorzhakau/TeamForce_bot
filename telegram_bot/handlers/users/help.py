from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    """Ответ на запрос команды help."""
    text = (
        "Список команд: ",
        "/start - Начать диалог",
        "/menu - Главное меню",
        "/help - Получить справку",
    )
    await message.answer("\n".join(text))
