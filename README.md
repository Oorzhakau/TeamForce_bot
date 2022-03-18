# TeamForce_bot
## Описание
Бот для хакатона TeamForce (Кейс № 3)

Telegram-bot получает сообщения по конкретной теме/проекту от внешних (в том числе новых) корреспондентов, накапливать их и буферизировать в БД.

В отличие от групп, потоки сообщений от каждого корреспондента изолированы между собой, но видны одним потоком пользователю, инициирующему запуск робота (то есть истинному получателю сообщений).

Бот реализован на базе PostgreSQL и Django ORM, с возможностью взаимодействовать с базой через админ-панель Django.
<img src="media/Django.JPG" alt="django" border="1">

Логика телеграм-бота реализована с помощью ассинхронного фреймворка aiogram.

Для ознакомление с проектом можно перейти на бота по ссылке https://t.me/ForceAlliance_bot

## Технологии
* Python 3.8
* Django 4.0
* PostgreSQL 4.0
* Aiogram 2.19
* Docker 3.1

## Запуск проекта в dev-режиме
- Устанавливаете docker и docker-compose;
```
sudo apt update
sudo apt install docker docker-compose -y
```
- Переименовываете файл .env_example на .env и заполняете его нужными значениями переменных окружения.<br>
Help по токенам
    <ul>
       <li><a href="https://core.telegram.org/bots#6-botfather">Токен телеграмм-бота</a></li>
       <li>Ваш telegram id можно узнать у бота @userinfobot</li>
    </ul>
- В папке проекта запускаете docker-compose:

```
docker-compose up --build
```
- По адресу localhost:8003/admin/ переходим в панель и входим под ранее созданным superuser-ом;
<img src="media/Django_admin.JPG" alt="django-admin" border="1">

- Проект запущен и готов к работе.

### Список исполнителей
* [Александр Ооржак](https://github.com/Oorzhakau) (telegram @oorzhakau)
* Валерия Алексеевна Аксенова (telegram @vlr787)