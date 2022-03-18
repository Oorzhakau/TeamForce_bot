import logging

from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message

from loader import dp


@dp.message_handler(Command("about"))
@dp.message_handler(Text(equals="О нас 🧙 и проекте"))
async def about_us(message: Message):
    """Реализация ответа на сообщение 'О нас'."""
    text = "\n".join(
        [
            "<b>Хакатон TeamForse</b>\n",
            "Вебсайт: https://tfalliance.ru/\n",
            "Кейс № 3\n",
            "Команда \"Удача\"🍀\n",
            "👨‍⚕️ 📞 Бот-ассистент, который получает сообщения по конкретной теме/проекту" +
            "от внешних (в том числе новых) корреспондентов, накапливать их и буферизировать в БД," +
            "далее пересылая владельцу бота данные сообщения в едином потоке.\n",
        ]
    )
    await message.answer(text=text)
    logging.info(text)
