from aiogram.dispatcher.filters.state import State, StatesGroup


class TagState(StatesGroup):
    """Класс машины состояния для создания темы."""
    tag = State()

