import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
import logging

from keyboards.default.cancel_menu import cancel_menu
from keyboards.default.sub_menu import sub_menu
from keyboards.default.admin_menu import admin_menu

from filters.filters_admin import IsAdmin
from loader import dp
from utils.db_api import db_commands as commands
from data.config import ADMIN
from states.state_distrib import DistGroupState, DistSubState


loop = asyncio.get_event_loop()
coroutine = commands.get_user()
User = loop.run_until_complete(coroutine)


@dp.message_handler(IsAdmin(), text="Отправить сообщение корреспонденту(-ам)📩")
async def bot_send_message_to_group_initial(message: types.Message):
    '''handler для формирования рассылки сообщения группе'''
    await message.answer(
        "Введите <b>username</b> корреспондентов через запятую "
        + "(username1,username2,username3 и т.д.):"
    )
    await DistGroupState.group.set()


@dp.message_handler(IsAdmin(), state=DistGroupState.group)
async def bot_send_message_to_group_take_usernames(message: types.Message, state: FSMContext):
    '''handler отправки сообщения группе.'''
    group = message.text.lower().strip().split(',')
    for sub in group:
        if not await commands.check_exist_username(sub):
            await message.answer(
                "Введен некорректный username. "
                + "Повторите попытку "
                + "или отмените заявку.",
                reply_markup=cancel_menu,
            )
            return
    await state.update_data(
        {"group": group}
    )
    await message.answer(f"<b>Введите сообщение для группы:</b>")
    await DistGroupState.next()


@dp.message_handler(IsAdmin(), state=DistGroupState.message)
async def bot_message_group_send(message: types.Message, state: FSMContext):
    '''handler отправки сообщения группе.'''
    text = message.text
    data = await state.get_data()
    subs = await commands.get_subs_in_group(data["group"])
    await commands.add_message(
        text=text,
        author=await commands.get_subscriber(User.user_id),
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
    await message.answer(
        text="Сообщение отправлено корреспондентам!",
        reply_markup=admin_menu,
    )
    await state.finish()


@dp.message_handler(IsAdmin(), text="Отправить сообщение пользователю 📩")
async def bot_message_user(message: types.Message):
    '''handler для отправки сообщения пользователю.'''
    await message.answer(
        "Введите <b>username</b> пользователя:"
    )
    await DistSubState.sub.set()


@dp.message_handler(IsAdmin(), state=DistSubState.sub)
async def bot_message_input_username(message: types.Message, state: FSMContext):
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
    await message.answer(f"<b>Кому:</b> {username}\n<b>Введите сообщение:</b>")
    await DistSubState.next()


@dp.message_handler(IsAdmin(), state=DistSubState.message)
async def bot_message_send_message_to_user(message: types.Message, state: FSMContext):
    '''handler отправка сообщения пользователю.'''
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
