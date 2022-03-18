from aiogram.dispatcher.filters.state import State, StatesGroup


class MessageState(StatesGroup):
    """Класс машины состояния для создания темы."""
    tag = State()
    message = State()
    
