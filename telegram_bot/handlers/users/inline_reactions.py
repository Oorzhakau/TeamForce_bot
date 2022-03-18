import logging

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.react_buttons import choice
from loader import dp


@dp.callback_query_handler(text="received")
async def received_message_to_subscriber(call: CallbackQuery):

    await call.message.edit_reply_markup(reply_markup=None)


@dp.callback_query_handler(text="delete")
async def delete_mmessage(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)