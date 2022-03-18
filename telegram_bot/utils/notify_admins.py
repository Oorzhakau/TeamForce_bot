import logging
import os

from aiogram import Dispatcher


async def on_startup_notify(dp: Dispatcher):
    """Оповещение администраторов о запуске бота."""
    admin = int(os.environ.get("ADMIN"))
    try:
        await dp.bot.send_message(admin, "Бот Запущен")

    except Exception as err:
        logging.exception(err)
