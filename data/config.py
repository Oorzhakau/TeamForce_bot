"""Загрузка переменных окружения."""
from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMIN = env.int("ADMIN")
DEBUG = env.list("DEBUG")

DJANGO_ALLOWED_HOSTS = env.str("DJANGO_ALLOWED_HOSTS")
SECRET_KEY = env.str("SECRET_KEY")

POSTGRES_DB = env.str("POSTGRES_DB")
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")

POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
