import logging
import re
import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from keyboards.default.cancel_menu import cancel_menu

from keyboards.inline.callback_datas import tag_callback
from keyboards.inline.react_buttons import tag_choices

from filters.filters_admin import NotAdmin, IsAdmin
from loader import dp
from utils.db_api import db_commands as commands
from states.state_tag import TagState
from data.config import ADMIN


@dp.message_handler(text="Список тем 📁")
async def show_tags(message: Message):
    """Вывод списка тем доступных пользователю."""
    tags = await commands.get_all_tags(message.from_user.id)
    if tags:
        for tag in tags:
            await message.answer(
                text=str(tag),
                reply_markup=tag_choices,
            )
        return
    await message.answer(text="Список тем пуст!")
    logging.info("Отправлен список тем!")


@dp.message_handler(text="Список корреспондентов 📁")
async def show_subs(message: Message):
    """Вывод списка корреспондентов."""
    subs = await commands.get_all_subscribers()
    if subs:
        for sub in subs:
            await message.answer(sub.username)
        return
    await message.answer(text="Корреспондентов нет!")
    logging.info("Отправлен список коррекспондентов.")


@dp.message_handler(IsAdmin(), text="Добавить тему 📁")
async def add_tags(message: Message):
    """Добавить тему."""
    await message.answer(text="Введите название темы:")
    await TagState.tag.set()


@dp.message_handler(IsAdmin(), state=TagState.tag)
async def get_tag(message: Message, state: FSMContext):
    """Регистрация темы."""
    tag_title = message.text
    pattern = re.compile(
        "[A-Яа-яA-z0-9@,.!? ]+"
    )
    if not re.fullmatch(pattern, tag_title):
        await message.answer(
            "Введен некорректное название темы "
            + "(допустимые символы в названии [A-Яа-яA-z0-9@,.!?]). "
            + "Повторите попытку "
            + "или отмените заявку.",
            reply_markup=cancel_menu,
        )
        return
    await state.finish()
    tag = await commands.get_or_create_tag(tag_title)
    if tag is None:
        await message.answer(text="Тема создана.")
        return
    await message.answer("Тема уже существует.")


@dp.callback_query_handler(tag_callback.filter(operation="delete"))
async def buying_apples(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    tag = call.message.text
    await commands.delete_tags(tag)
    await call.message.delete()
    logging.info(f"{callback_data=}")
