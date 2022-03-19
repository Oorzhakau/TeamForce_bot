import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
import logging

from keyboards.default.cancel_menu import cancel_menu
from keyboards.default.sub_menu import sub_menu

from filters.filters_admin import IsAdmin
from loader import dp
from utils.db_api import db_commands as commands
from data.config import ADMIN
from states.state_distrib import DistGroupState, DistSubState


loop = asyncio.get_event_loop()
coroutine = commands.get_user()
User = loop.run_until_complete(coroutine)


@dp.message_handler(IsAdmin(), text="Рассылка группе 📩")
async def bot_message(message: types.Message):
    '''handler для формирования рассылки сообщения группе'''
    await message.answer(
        "Введите <b>группу</b> для которой нужно отправить сообщение:"
    )
    await DistGroupState.group.set()


@dp.message_handler(IsAdmin(), state=DistGroupState.group)
async def bot_message(message: types.Message, state: FSMContext):
    '''handler отправки сообщения группе.'''
    group = message.text
    if not await commands.check_exist_group(group):
        await message.answer(
            "Введено некорректное название группы. "
            + "Повторите попытку "
            + "или отмените заявку.",
            reply_markup=cancel_menu,
        )
        return
    await state.update_data(
        {"group": group}
    )
    await message.answer(f"<b>Группа:</b>{group}\nВведите сообщение:")
    await DistGroupState.next()


@dp.message_handler(IsAdmin(), state=DistGroupState.message)
async def bot_message(message: types.Message, state: FSMContext):
    '''handler отправки сообщения группе.'''
    text = message.text
    data = await state.get_data()
    subs = await commands.get_subs_in_group(data["group"])
    await commands.add_message(
        text=text,
        author=await commands.get_subscriber(User.user_id)
    )
    for sub in subs:
        await dp.bot.send_message(
            chat_id=sub.user_id,
            text='\n'.join(
                [
                    f"<b>От кого</b>: {message.from_user.username}",
                    f"<pre>{text}</pre>"
                ]
            )
        )
    await message.answer("Сообщение отправлено корреспондентам!")
    await state.finish()


@dp.message_handler(IsAdmin(), text="Отправить сообщение пользователю 📩")
async def bot_message(message: types.Message):
    '''handler для отправки сообщения пользователю.'''
    await message.answer(
        "Введите <b>username</b> пользователя:"
    )
    await DistSubState.sub.set()


@dp.message_handler(IsAdmin(), state=DistSubState.sub)
async def bot_message(message: types.Message, state: FSMContext):
    '''handler отправки сообщения пользователю.'''
    username = message.text
    if not await commands.check_exist_username(username):
        await message.answer(
            "Введен некорректный username. "
            + "Повторите попытку "
            + "или отмените заявку.",
            reply_markup=cancel_menu,
        )
        return
    await state.update_data(
        {"username": username}
    )
    await message.answer(f"<b>Кому:</b>{username}\nВведите сообщение:")
    await DistSubState.next()


@dp.message_handler(IsAdmin(), state=DistSubState.message)
async def bot_message(message: types.Message, state: FSMContext):
    '''handler отправки сообщения пользователю.'''
    text = message.text
    data = await state.get_data()
    sub = await commands.get_subscriber_by_username(data["username"])
    await commands.add_message(
        text=text,
        author=await commands.get_subscriber(User.user_id)
    )
    await dp.bot.send_message(
        chat_id=sub.user_id,
        text='\n'.join(
            [
                f"<b>От кого</b>: {message.from_user.username}",
                f"<pre>{text}</pre>"
            ]
        )
    )
    await message.answer(f"Сообщение отправлено <b>{sub.username}</b>!")
    await state.finish()
