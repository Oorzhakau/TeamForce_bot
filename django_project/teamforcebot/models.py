import os
from pyexpat import model
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict


class TimedBaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Group(models.Model):
    name = models.CharField(
        max_length=25,
        verbose_name='Название',
        blank=True,
    )
    
    class Meta:
        verbose_name = 'Кластер'
        verbose_name_plural = 'Кластеры'

    def __str__(self):
        return self.name


class User(AbstractUser):
    user_id = models.BigIntegerField(
        verbose_name='ID Пользователя Телеграм',
        unique=True,
        default=int(os.environ.get("ADMIN")),
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.id} {self.username}'


class Subscriber(models.Model):
    user_id = models.BigIntegerField(
        verbose_name='ID Пользователя Телеграм',
        unique=True,
    )
    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='email',
        blank=True,
        null=True,
    )
    phone = models.CharField(
        max_length=12,
        verbose_name='Телефон',
        blank=True,
        null=True,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    company = models.CharField(
        max_length=100,
        verbose_name='Компания',
        blank=True,
        null=True
    )
    notes = models.TextField(
        verbose_name='Заметки',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        default_related_name = 'subscribers'
    
    def __str__(self):
        return f'(tel id {self.user_id}) {self.username}'


class Tag(models.Model):
    tag = models.CharField(
        max_length=100,
        verbose_name='Тема сообщения',
    )
    subscribers = models.ManyToManyField(
        Subscriber
    )

    class Meta:
        ordering = ['tag']
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        default_related_name = 'tags'

    def __str__(self):
        return self.tag


class Message(TimedBaseModel):
    author = models.ForeignKey(
        Subscriber,
        null=True,
        on_delete=models.SET_NULL,
        related_name='message',
    )
    text = models.TextField(verbose_name='Сообщение', )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='message',
        blank=True,
        null=True,
    )
    status = models.BooleanField(
        verbose_name='Статус',
        default=False,
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.text[:15]