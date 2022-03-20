from aiogram.dispatcher.filters.state import State, StatesGroup


class SubState(StatesGroup):
    """Класс машины состояния для записи корреспондента."""

    sub = State()


class SelectMessageBySubState(StatesGroup):
    """Класс машины состояния для получения сообщений
    от корреспондента."""

    sub = State()
