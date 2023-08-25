import asyncio

from asgiref.sync import sync_to_async
from django.db import models

from .handlers.replys import send_reply_message


# модель пользователя
class User(models.Model):

    chat_id = models.BigIntegerField(verbose_name='ID пользователя', primary_key=True)
    user_login = models.CharField(verbose_name='Логин', max_length=255, unique=True)
    user_password = models.CharField(verbose_name='Пароль', max_length=128)
    is_registered = models.BooleanField(verbose_name='Зарегистрирован', default=False)
    registered_at = models.DateTimeField(verbose_name='Время регистрации', auto_now_add=True)

    def __str__(self):
        return self.user_login

    class Meta:
        verbose_name = 'Телеграм Пользователь'
        verbose_name_plural = 'Телеграм Пользователи'
        ordering = ['-registered_at']


#модель товара
class Product(models.Model):

    photo = models.ImageField(verbose_name='Фотография', upload_to='products/', blank=True)
    name = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание', blank=False)
    price = models.PositiveIntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Время редактирования', auto_now=True)
    is_published = models.BooleanField(verbose_name='Опубликован', default=True)
    #cвязь "многие ко многим" открывает какие покупатели купили данный товар
    user = models.ManyToManyField(User, default=None, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']


#Модель комментария. Комментарий доступен для клиента, купившего товар
class Comment(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=350, blank=True, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']


#Модель для сообщений приходящих от пользователей
#В ней поля для файлов и изображений
class Message(models.Model):

    message_id = models.BigIntegerField(verbose_name='ID сообщения', primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(blank=True, null=True, verbose_name='Текст')
    image = models.ImageField(blank=True, upload_to='images/')
    file = models.FileField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата, время сообщения')

    def __str__(self):
        return f'{self.user}:{self.text}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


#Модель для ответа на сообщения пользователей напрямую из админки
class Reply(models.Model):

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    text = models.TextField(max_length=250, blank=True, verbose_name='Текст сообщения')
    image = models.ImageField(blank=True, verbose_name='Картинка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата, время сообщения')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы на сообщения'

