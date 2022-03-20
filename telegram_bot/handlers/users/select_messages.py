import logging
import re
import os

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.default.cancel_menu import cancel_menu
from keyboards.default.admin_menu import admin_menu
from filters.filters_admin import IsAdmin
from loader import dp
from utils.db_api import db_commands as commands
from states.state_tag import SelectMessageByTagState
from states.state_sub import SelectMessageBySubState
from data.config import ADMIN
from keyboards.inline.callback_datas import message_callback
from keyboards.inline.react_buttons import message_choices


@dp.message_handler(IsAdmin(),
                    text="Список cообщений на конкретную тему 💬")
async def select_tags(message: Message):
    """Handler запроса темы."""
    await message.answer(text="Введите тему")
    await SelectMessageByTagState.tag.set()


@dp.message_handler(IsAdmin(), state=SelectMessageByTagState.tag)
async def return_messages_with_tag(message: Message, state: FSMContext):
    """Handler возврата сообщений с определенной темой."""
    tag = message.text
    if not await commands.check_exist_tag(tag):
        await message.answer(
            "Введено некорректное название темы. "
            + "Повторите попытку "
            + "или отмените заявку.",
            reply_markup=cancel_menu,
        )
        return
    messages = await commands.get_messages_with_tag(tag)
    if messages:
        for msg in messages:
            await message.answer(
                text=f"{msg.text}",
                reply_markup=message_choices,
            )
        await state.finish()
        return
    await message.answer(f"Сообщений на тему <b>{tag}</b> нет!")
    await state.finish()


@dp.message_handler(IsAdmin(),
                    text="Список сообщений от корреспондента 👨‍⚕️")
async def select_sub(message: Message):
    """Handler запроса username."""
    await message.answer(text="Введите username:")
    await SelectMessageBySubState.sub.set()


@dp.message_handler(IsAdmin(), state=SelectMessageBySubState.sub)
async def return_messages_by_sub(message: Message, state: FSMContext):
    """Handler возврата сообщений от корреспондента."""
    sub = message.text
    if not await commands.check_exist_username(sub):
        await message.answer(
            "Введено некорректный username. "
            + "Повторите попытку "
            + "или отмените заявку.",
            reply_markup=cancel_menu,
        )
        return
    messages = await commands.get_messages_from_sub(sub)
    if messages:
        for msg in messages:
            await message.answer(
                text=msg.text,
                reply_markup=message_choices,
            )
        await state.finish()
        return
    await message.answer(f"Сообщений от <b>{sub}</b> нет!")
    await state.finish()


@dp.callback_query_handler(message_callback.filter(operation="delete"))
async def buying_apples(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f"{callback_data=}")
    text = call.message.text
    await commands.delete_message_by_text(text)
    await call.message.delete()
