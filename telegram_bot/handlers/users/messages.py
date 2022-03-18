import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
import logging

from keyboards.default.cancel_menu import cancel_menu
from keyboards.default.sub_menu import sub_menu

from filters.filters_admin import NotAdmin
from loader import dp
from utils.db_api import db_commands as commands
from data.config import ADMIN
from aiogram.dispatcher.filters import Command, Text
from states.state_message import MessageState


loop = asyncio.get_event_loop()
coroutine = commands.get_user()
User = loop.run_until_complete(coroutine)


@dp.message_handler(NotAdmin(), text="Написать сообщение 📝")
async def bot_message(message: types.Message):
    '''handler для формирования сообщения'''
    await message.answer("Введите <b>тему</b> сообщения (из списка тем):")
    await MessageState.tag.set()


@dp.message_handler(NotAdmin(), state=MessageState.tag)
async def bot_message(message: types.Message, state: FSMContext):
    '''handler для указания темы сообщения.'''
    tag = message.text
    if not await commands.check_exist_tag(tag):
        await message.answer(
            "Введено некорректное название темы. "
            + "Повторите попытку "
            + "или отмените заявку.",
            reply_markup=cancel_menu,
        )
        return
    await state.update_data(
        {"tag": tag}
    )
    await message.answer(f"<b>Тема:{tag}<b><br>Введите сообщение:")
    await MessageState.next()


@dp.message_handler(NotAdmin(), state=MessageState.message)
async def bot_message(message: types.Message, state: FSMContext):
    '''handler для записи сообщений от подписчиков в базу данных'''
    text = message.text
    data = await state.get_data()
    tag = await commands.get_tag(data["tag"])
    author = await commands.get_subscriber(message.from_user.id)
    await commands.add_message(author=author, text=text, tag=tag)
    await message.answer(
        "\n".join(
            [
                f"Сообщение добавлено в базу.",
                f"<i>От кого</i>: {message.from_user.full_name}",
                f"<i>Кому</i>: {User.first_name} {User.last_name}",
                f"<i>Тема:</i>: {tag}",
                f"<pre>{message.text}</pre>",
            ]
        ),
        reply_markup=sub_menu
    )
    await dp.bot.send_message(
        chat_id=ADMIN,
        text='\n'.join(
            [
                f"<i>От кого</i>: {message.from_user.username}",
                f"<i>Тема</i>: {tag}",
                f"<pre>{text}</pre>"
            ]
        )
    )
    await state.finish()
