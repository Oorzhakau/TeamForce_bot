from aiogram.dispatcher.filters.state import State, StatesGroup


class TagState(StatesGroup):
    """Класс машины состояния для создания темы."""

    tag = State()


class SelectMessageByTagState(StatesGroup):
    """Класс машины состояния для получения сообщений по темам."""

    tag = State()


class AddSubscribersToTag(StatesGroup):
    """Машина состояния для добавления subscribers в топик"""

    tag = State()
    subscribers = State()
