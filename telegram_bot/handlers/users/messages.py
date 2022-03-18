import asyncio
from aiogram import types
from filters.not_admin import NotAdmin
from loader import dp
from utils.db_api import db_commands as commands
from data.config import ADMIN
from aiogram.dispatcher.filters import Command, Text
import logging


loop = asyncio.get_event_loop()
coroutine = commands.get_user()
User = loop.run_until_complete(coroutine)


@dp.message_handler(NotAdmin())
async def bot_message(message: types.Message):
    '''handler для записи сообщений от подписчиков в базу данных'''
    text = message.text
    author = await commands.get_subscriber(message.from_user.id)
    await commands.add_message(author=author, text=text)
    await message.answer(
        "\n".join(
            [
                f"Сообщение добавлено в базу",
                f"<i>From user</i>: {message.from_user.full_name}",
                f"<i>To user</i>: {User.first_name} {User.last_name}",
                f"<pre>{message.text}</pre>",
            ]
        )
    )
    await dp.bot.send_message(
        chat_id=ADMIN,
        text='\n'.join(
            [
                f"<i>From user</i>: {message.from_user.username}"
                f"<pre>{text}</pre>"
            ]
        )
    )