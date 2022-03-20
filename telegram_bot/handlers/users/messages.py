import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMIN
from filters.filters_admin import NotAdmin
from keyboards.default.cancel_menu import cancel_menu
from keyboards.default.sub_menu import sub_menu
from loader import dp
from states.state_message import MessageState
from utils.db_api import db_commands as commands

loop = asyncio.get_event_loop()
coroutine = commands.get_user()
User = loop.run_until_complete(coroutine)


@dp.message_handler(NotAdmin(), text="Написать сообщение 📝")
async def bot_write_message_initial(message: types.Message):
    """handler для формирования сообщения."""
    await message.answer("Введите <b>тему</b> сообщения (из списка тем):")
    await MessageState.tag.set()


@dp.message_handler(NotAdmin(), state=MessageState.tag)
async def bot_write_message_get(message: types.Message, state: FSMContext):
    """handler для указания темы сообщения."""
    tag = message.text
    if not await commands.check_sub_tags(tag, message.from_user.id):
        await message.answer(
            "Введено некорректное название темы. "
            + "Повторите попытку "
            + "или отмените заявку.",
            reply_markup=cancel_menu,
        )
        return
    await state.update_data({"tag": tag})
    await message.answer(f"<b>Тема:</b>{tag}\nВведите сообщение:")
    await MessageState.next()


@dp.message_handler(NotAdmin(), state=MessageState.message)
async def bot_message(message: types.Message, state: FSMContext):
    """handler для записи сообщений от подписчиков в базу данных."""
    text = message.text
    data = await state.get_data()
    tag = await commands.get_tag(data["tag"])
    author = await commands.get_subscriber(message.from_user.id)
    await commands.add_message(author=author, text=text, tag=tag)
    await message.answer(
        "\n".join(
            [
                "Сообщение добавлено в базу.",
                f"<b>От кого</b>: {message.from_user.full_name}",
                f"<b>Тема:</b>: {tag}",
                f"<pre>{message.text}</pre>",
            ]
        ),
        reply_markup=sub_menu,
    )
    await dp.bot.send_message(
        chat_id=ADMIN,
        text="\n".join(
            [
                f"<b>От кого</b>: {message.from_user.user_id} "
                + f"{message.from_user.full_name}",
                f"<b>Тема</b>: {tag}",
                f"<pre>{text}</pre>",
            ]
        ),
    )
    await state.finish()
