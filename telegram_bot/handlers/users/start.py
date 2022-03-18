import asyncio
import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.admin_menu import admin_menu
from keyboards.default.sub_menu import sub_menu
from loader import dp
from utils.db_api import db_commands as commands
from data.config import ADMIN


loop = asyncio.get_event_loop()
coroutine = commands.get_user()
User = loop.run_until_complete(coroutine)

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    """Handler для запуска бота."""
    chat_id = message.from_user.id
    logging.info(f"Бот активирован пользователем telegram id - {chat_id}")
    menu = admin_menu if message.from_user.id == ADMIN else sub_menu
    if chat_id == ADMIN:
        await message.answer(
            "\n".join(
            [
                f'Здравствуйте, <b>{message.from_user.username}</b>!',
                f'Бот-ассистент активирован!',
            ]),
            reply_markup=menu
        )
        return
    subscriber = await commands.get_subscriber(message.from_user.id)
    if not subscriber:
        subscriber = await commands.add_subscriber(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )
        count = await commands.get_count_subscribers()
        await message.answer(
            "\n".join(
                [
                    f'Здравствуйте, <b>{message.from_user.full_name}</b>!',
                    f'Вы были занесен в базу для отправки сообщений',
                    f'пользователю: <b>{User.first_name} {User.last_name}</b>',
                    f'telegram id: <b>{User.user_id}</b>',
                    f'В базе <b>{count}</b> пользователей',
                ]
            ),
            reply_markup=menu,
        )
        return
    await message.answer(f"Здравствуйте, <b>{message.from_user.username}</b>!")
