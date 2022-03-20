from aiogram.dispatcher.filters.state import State, StatesGroup


class DistGroupState(StatesGroup):
    """Класс машины состояния выбора группы для отправки сообщения."""

    group = State()
    message = State()


class DistSubState(StatesGroup):
    """Класс машины состояния отправки сообщения корреспонденту."""

    sub = State()
    message = State()
