import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from filters.filters_admin import IsAdmin
from keyboards.default.cancel_menu import cancel_menu
from keyboards.inline.callback_datas import message_callback
from keyboards.inline.react_buttons import message_choices
from loader import dp
from states.state_sub import SelectMessageBySubState
from states.state_tag import SelectMessageByTagState
from utils.db_api import db_commands as commands


@dp.message_handler(IsAdmin(), text="Список cообщений на конкретную тему 💬")
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
            from_user = [
                str(msg.author.user_id),
                msg.author.username,
                msg.author.first_name,
                msg.author.last_name,
            ]
            from_user = " ".join(
                list(filter(lambda item: not (item is None), from_user))
            )
            await message.answer(
                text="\n".join(
                    [
                        f"<b>От кого</b>: {from_user}",
                        f"<b>Тема</b>: {msg.tag}",
                        f"{msg.text}",
                    ]
                ),
                reply_markup=message_choices,
            )
        await state.finish()
        return
    await message.answer(f"Сообщений на тему <b>{tag}</b> нет!")
    await state.finish()


@dp.message_handler(IsAdmin(), text="Список сообщений от корреспондента 👨‍⚕️")
async def select_sub(message: Message):
    """Handler запроса username."""
    await message.answer(text="Введите user_id:")
    await SelectMessageBySubState.sub.set()


@dp.message_handler(IsAdmin(), state=SelectMessageBySubState.sub)
async def return_messages_by_sub(message: Message, state: FSMContext):
    """Handler возврата сообщений от корреспондента."""
    user_id = int(message.text)
    if not await commands.check_exist_user_id(user_id):
        await message.answer(
            "Введено некорректный username. "
            + "Повторите попытку "
            + "или отмените заявку.",
            reply_markup=cancel_menu,
        )
        return
    messages = await commands.get_messages_from_sub_by_user_id(user_id)
    if messages:
        from_user = [
            str(messages[0].author.user_id),
            messages[0].author.username,
            messages[0].author.first_name,
            messages[0].author.last_name,
        ]
        from_user = " ".join(
            list(filter(lambda item: not (item is None), from_user))
        )
        for msg in messages:
            await message.answer(
                text="\n".join(
                    [
                        f"<b>От кого</b>: {from_user}",
                        f"<b>Тема</b>: {msg.tag}",
                        f"{msg.text}",
                    ]
                ),
                reply_markup=message_choices,
            )
        await state.finish()
        return
    await message.answer("Сообщений нет!")
    await state.finish()


@dp.callback_query_handler(message_callback.filter(operation="delete"))
async def buying_apples(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f"{callback_data=}")
    text = call.message.text
    text = text.split("\n")[-1]
    await commands.delete_message_by_text(text)
    await call.message.delete()
