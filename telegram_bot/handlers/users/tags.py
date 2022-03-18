import logging
import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.default.cancel_menu import cancel_menu
from loader import dp
from utils.db_api import db_commands as commands
from states.state_tag import TagState


@dp.message_handler(Text(startswith="❌Отменить"), state="*")
async def cancel_application(message: Message, state: FSMContext):
    """Реализация функции кнопки отмены."""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer(
        "Отмена операции.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message_handler(Text(equals="Список тем 📁"))
async def show_tags(message: Message):
    """Вывод списка тем."""
    tags = await commands.get_all_tags()
    if tags:
        for tag in tags:
            await message.answer(text=str(tag))
        return
    await message.answer(text="Список тем пуст!")
    logging.info("Отправлен список тем!")


@dp.message_handler(Text(equals="Добавить тему 📁"))
async def add_tags(message: Message):
    """Добавить тему."""
    tags = await commands.add_tag()
    await message.answer(text="Введите название темы:")
    await TagState.email.set()


# @dp.message_handler(state=TagState.tag)
# async def get_email(message: Message, state: FSMContext):
#     """Получение электронной почты для заявки."""
#     tag_title = message.text
#     pattern = re.compile(
#         "[A-Za-z0-9]+"
#     )
#     if not re.fullmatch(pattern, tag_title):
#         await message.answer(
#             "Введен некорректный email. Повторите попытку "
#             + "или отмените заявку.",
#             reply_markup=cancel_menu,
#         )
#         return
#     await state.finish()
#     tag = 
#     await message.answer(
#         "Введите ваше имя",
#         reply_markup=cancel_menu,
#     )
#     await RequestState.next()