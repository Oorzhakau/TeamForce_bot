from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove
from loader import dp


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
