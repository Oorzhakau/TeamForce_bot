import asyncio
import os
from aiogram import types
from aiogram.dispatcher import FSMContext
import logging

from keyboards.default.cancel_menu import cancel_menu
from keyboards.default.sub_menu import sub_menu

from filters.filters_admin import NotAdmin
from loader import dp
from utils.db_api import db_commands as commands
from data.config import ADMIN
from states.state_message import MessageState


loop = asyncio.get_event_loop()
coroutine = commands.get_user()
User = loop.run_until_complete(coroutine)


@dp.message_handler(text="Ссылка на бота")
async def bot_message(message: types.Message):
    '''handler для отправки ссылки на бота'''
    bot_name = os.environ.get("BOT_NAME")
    await message.answer(f"Ссылка на бота - https://t.me/{bot_name}")