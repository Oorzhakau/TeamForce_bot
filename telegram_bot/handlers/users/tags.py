import re

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from data.config import ADMIN

from filters.filters_admin import IsAdmin
from keyboards.default.admin_menu import admin_menu
from keyboards.default.cancel_menu import cancel_menu
from keyboards.default.sub_menu import sub_menu
from keyboards.inline.callback_datas import tag_callback
from loader import dp
from states.state_tag import AddSubscribersToTag, TagState
from utils.db_api import db_commands as commands


@dp.message_handler(text="Список тем 📁")
async def show_tags(message: Message):
    """Вывод списка тем доступных пользователю."""
    tags = await commands.get_all_tags(message.from_user.id)
    menu = admin_menu if message.from_user.id == ADMIN else sub_menu
    if tags:
        for tag in tags:
            await message.answer(
                text=str(tag),
                reply_markup=menu,
            )
        return
    await message.answer(text="Список тем пуст!")


@dp.message_handler(text="Список корреспондентов 📁")
async def show_subs(message: Message):
    """Вывод списка корреспондентов."""
    subs = await commands.get_all_subscribers()
    if subs:
        for sub in subs:
            await message.answer(
                "\n".join(
                    [
                        f"<b>User id:</b>{sub.user_id}",
                        f"<b>Username:</b>{sub.username}",
                        f"<b>First name:</b>{sub.first_name}",
                        f"<b>Last name:</b>{sub.last_name}",
                    ]
                )
            )
        return
    await message.answer(text="Корреспондентов нет!")


@dp.message_handler(IsAdmin(), text="Добавить тему 📁")
async def add_tags(message: Message):
    """Добавить тему."""
    await message.answer(text="Введите название темы:")
    await TagState.tag.set()


@dp.message_handler(IsAdmin(), state=TagState.tag)
async def get_tag(message: Message, state: FSMContext):
    """Регистрация темы."""
    tag_title = message.text
    pattern = re.compile("[A-Яа-яA-z0-9@,.!? ]+")
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
async def inline_tag_deletes(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    tag = call.message.text
    await commands.delete_tags(tag)
    await call.message.delete()


@dp.message_handler(IsAdmin(), text="Добавить корреспондента(-ов) в тему")
async def add_subscribers_to_tag_initial(message: Message):
    await message.answer(text="Введите название темы:")
    await AddSubscribersToTag.tag.set()


@dp.message_handler(IsAdmin(), state=AddSubscribersToTag.tag)
async def add_subscribers_to_tag_get_tag(message: Message, state: FSMContext):
    tag = message.text
    if not await commands.check_exist_tag(tag):
        await message.answer(
            "Введена некорректная тема. "
            + "Повторите попытку "
            + "или отмените заявку.",
            reply_markup=cancel_menu,
        )
        return
    await state.update_data({"tag": tag})
    await message.answer(
        "Укажите через запятую без пробелов user_id коррекспондентов, "
        + "кто должен иметь доступ к указанной теме  "
        + "(user_id1,user_id2,user_id3 и т.д.):"
    )
    await AddSubscribersToTag.next()


@dp.message_handler(IsAdmin(), state=AddSubscribersToTag.subscribers)
async def add_subscribers_to_tag_get_users_id(
    message: Message, state: FSMContext
):
    group = [int(user_id) for user_id in message.text.strip().split(",")]
    data = await state.get_data()
    for sub in group:
        if not await commands.check_exist_user_id(sub):
            await message.answer(
                f"{sub} отсутствует в базе бота. "
                + "Повторите попытку "
                + "или отмените заявку.",
                reply_markup=cancel_menu,
            )
            return
    tag = await commands.get_tag(data["tag"])
    group = await commands.get_subs_in_group_by_user_id(group)
    await commands.add_subscribers_to_tag(tag, group)
    for sub in group:
        await dp.bot.send_message(
            chat_id=sub.user_id,
            text="\n".join(
                [
                    f"<b>От кого</b>: {message.from_user.username}",
                    f"<pre>Вы были добавлены в тему: <b>{data['tag']}</b></pre>",
                ]
            ),
        )
    await message.answer("Пользователи добавлены в тему.")
    await state.finish()
