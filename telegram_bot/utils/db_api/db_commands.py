"""Реализация базовых команд для асинхронного запроса к базе
данных Postgres через Django ORM.
"""

from genericpath import exists
import os
import sys
from pathlib import Path
from typing import List, Optional, Union

from asgiref.sync import sync_to_async

ROOT_DIR = Path(__file__).parents[3]
MODEL_PATH = os.path.join(ROOT_DIR, "django_project")
sys.path.append(MODEL_PATH)

from teamforcebot.models import User, Subscriber, Tag, Message


@sync_to_async
def add_subscriber(
    user_id: Union[str, int],
    username: str,
    first_name: Optional[str],
    last_name: Optional[str],
) -> Subscriber:
    """Добавить подписчика."""
    sub = Subscriber.objects.create(
        user_id=int(user_id),
        first_name=first_name,
        last_name=last_name,
        username=username,
    )
    sub.save()
    return sub


@sync_to_async
def get_all_subscribers() -> List[Subscriber]:
    """Получить всех подписчиков."""
    subs = Subscriber.objects.all()
    return subs


@sync_to_async
def get_subscriber(user_id: int) -> Optional[Subscriber]:
    """Получить подписчика по user_id."""
    if Subscriber.objects.filter(user_id=user_id).exists():
        subscriber = Subscriber.objects.get(user_id=user_id)
        return subscriber


async def get_then_update(
    user_id: int, name: str, email: str, phone: str
) -> Subscriber:
    """Получение и обновление подписчика."""
    subscriber = await get_subscriber(user_id)
    if not subscriber.first_name:
        subscriber.first_name = name
    if not subscriber.email:
        subscriber.email = email
    if not subscriber.phone:
        subscriber.phone = phone
    subscriber.save()
    return subscriber


@sync_to_async
def get_count_subscribers() -> int:
    """Получить число зарегистрированных подписчиков."""
    total = Subscriber.objects.count()
    return total


@sync_to_async
def add_message(**kwargs) -> Message:
    '''сохранение сообщения в базе'''
    message = Message(**kwargs).save()
    return message


@sync_to_async
def get_message_by_text(text: str) -> Optional[Message]:
    """Получить сообщение с указанным текстом."""
    message = Message.objects.get(text=text)
    return message


@sync_to_async
def delete_message_by_text(text: str) -> None:
    """Удалить сообщение с указанным текстом."""
    message = Message.objects.get(text=text)
    message.delete()


@sync_to_async
def get_messages_with_tag(tag: str) -> Optional[List[Optional[Message]]]:
    """Получить все сообщения с указанной темой."""
    messages = Message.objects.filter(tag__tag=tag)
    return messages


@sync_to_async
def get_messages_from_sub(username: str) -> Optional[List[Optional[Message]]]:
    """Получить все сообщения от username."""
    messages = Message.objects.filter(author__username=username)
    return messages


@sync_to_async
def get_all_messages() -> List[Message]:
    """Получить все сообщения."""
    messages = Message.objects.all()
    return messages


@sync_to_async
def get_count_messages() -> int:
    """Получить количество сообщений."""
    return Message.objects.count()


@sync_to_async
def create_tag(string: str) -> Tag:
    """Создать тему в базе"""
    tag = Tag(tag=string).save()
    return tag


@sync_to_async
def get_or_create_tag(string: str) -> Optional[Tag]:
    """Cохранение темы в базе"""
    tag = Tag.objects.filter(tag=string)
    if not tag.exists():
        Tag(tag=string).save()
        return None
    return tag


@sync_to_async
def get_all_tags() -> List[Tag]:
    """Получить все темы."""
    tags = Tag.objects.all()
    return tags


@sync_to_async
def get_tag(string: str) -> Tag:
    """Получить тему."""
    return Tag.objects.get(tag=string)


@sync_to_async
def check_exist_tag(tag: str) -> bool:
    """Проверить наличие темы."""
    return Tag.objects.filter(tag=tag).exists()


@sync_to_async
def check_exist_username(string: str) -> bool:
    """Проверить наличие темы."""
    return Subscriber.objects.filter(username=string).exists()


@sync_to_async
def delete_tags(tag: str) -> None:
    """Удалить тему."""
    tag = Message.objects.get(tag=tag)
    tag.delete()


@sync_to_async
def get_user() -> User:
    user_id = int(os.environ.get("ADMIN"))
    try:
        user = User.objects.get(user_id=user_id)
    except:
        user = User.objects.get(username="admin")
        user.user_id = user_id
        user.save()
    return user
