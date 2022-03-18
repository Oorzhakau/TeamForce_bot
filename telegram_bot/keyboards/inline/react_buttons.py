from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


choice = InlineKeyboardMarkup(row_width=2)

received_button = InlineKeyboardButton(text="Ознакомлен", callback_data="received")
choice.insert(received_button)

delete_button = InlineKeyboardButton(text="Удалить", callback_data="delete")
choice.insert(delete_button)