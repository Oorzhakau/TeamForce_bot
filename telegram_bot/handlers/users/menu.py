import logging
import os

from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from keyboards.default.admin_menu import admin_menu
from keyboards.default.sub_menu import sub_menu
from loader import dp
from data.config import ADMIN


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    """Функция отображения кнопок меню."""
    logging.info(f"Выполнение команды menu. User id {message.from_user.id}")
    menu = admin_menu if message.from_user.id == ADMIN else sub_menu
    # menu = sub_menu
    await message.answer("Главное меню", reply_markup=menu)
