import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters.filters_admin import IsAdmin
from keyboards.default.admin_menu import admin_menu
from keyboards.default.cancel_menu import cancel_menu
from loader import dp
from states.state_distrib import DistGroupState
from utils.db_api import db_commands as commands

loop = asyncio.get_event_loop()
coroutine = commands.get_user()
User = loop.run_until_complete(coroutine)


@dp.message_handler(IsAdmin(), text="Отправить сообщение корреспонденту(-ам)📩")
async def bot_send_message_to_group_initial(message: types.Message):
    """handler для формирования рассылки сообщения группе"""
    await message.answer(
        "Введите <b>user_id</b> корреспондентов через запятую без пробелов "
        + "(user_id1,user_id2,user_id3 и т.д.):"
    )
    await DistGroupState.group.set()


@dp.message_handler(IsAdmin(), state=DistGroupState.group)
async def bot_send_message_to_group_take_usernames(
    message: types.Message, state: FSMContext
):
    """handler отправки сообщения группе."""
    group = [int(user_id) for user_id in message.text.strip().split(",")]
    for sub in group:
        if not await commands.check_exist_user_id(sub):
            await message.answer(
                f"{sub} отсутствует в базе бота. "
                + "Повторите попытку "
                + "или отмените заявку.",
                reply_markup=cancel_menu,
            )
            return
    await state.update_data({"group": group})
    await message.answer("Введите сообщение:")
    await DistGroupState.next()


@dp.message_handler(IsAdmin(), state=DistGroupState.message)
async def bot_send_message_to_group_finish(
    message: types.Message, state: FSMContext
):
    """handler отправки сообщения группе."""
    text = message.text
    data = await state.get_data()
    subs = await commands.get_subs_in_group_by_user_id(data["group"])
    await commands.add_message(
        text=text,
        author=await commands.get_subscriber(User.user_id),
    )
    for sub in subs:
        await dp.bot.send_message(
            chat_id=sub.user_id,
            text="\n".join(
                [
                    f"<b>От кого</b>: {message.from_user.username}",
                    f"<pre>{text}</pre>",
                ]
            ),
        )
    await message.answer(
        text="Сообщение отправлено корреспондентам!",
        reply_markup=admin_menu,
    )
    await state.finish()
