"""
Запуск приложения телеграмм бота. Опрос сервера методом пулинга.
"""


def setup_django():
    import os
    import sys

    import django

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "django_project")
    sys.path.append(DATA_PATH)

    os.environ["DJANGO_SETTINGS_MODULE"] = "django_project.settings"
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()


async def on_startup(dispatcher):
    """Установка базовых команд и уведомления о включении бота."""
    from utils.notify_admins import on_startup_notify
    from utils.set_bot_commands import set_default_commands

    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


if __name__ == "__main__":
    setup_django()

    import middlewares
    import filters
    import handlers
    import asyncio

    from aiogram import executor
    from loader import dp

    from utils.db_api import db_commands as commands

    loop = asyncio.get_event_loop()
    coroutine = commands.get_user()
    loop.run_until_complete(coroutine)
    
    executor.start_polling(dp, on_startup=on_startup)
