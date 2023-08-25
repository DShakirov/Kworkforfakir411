import os
import re
from random import randrange

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import update, ContentType
from aiogram.utils import executor
from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password, check_password
from kworkforfakir411.settings import BOT_TOKEN

from . import settings
from .settings import ADMIN_ID
from .utils import *
from ..keyboards import sign_inup_kb, default_kb, admin_kb
from ..keyboards.registration_kb import markup, markup_cancel_forgot_password
from ..models import User, Message
from ..states import AuthState, SignInState, ForgotPasswordState

#создаем нашего бота и диспетчер, хранилище состояний
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Хендлер обратной связи - только текст
@dp.message_handler(Text(contains='Ф'))
async def cmd_message(message: types.Message):
#распарсим ответ и записываем сообщение в базу данных
    text = message['text']
    user_id = message['from']['id']
    message_id = message['message_id']
    await save_message(text, user_id, message_id, photo=None, file=None)
    # Отвечаем пользователю
    await message.answer(text='Спасибо за обратную связь\n Ваше сообщение сохранено', reply_markup=sign_inup_kb.markup)
#Пересылаем сообщение администратору
    if user_id != ADMIN_ID:
        await bot.forward_message(chat_id=ADMIN_ID, from_chat_id=user_id, message_id=message_id)


#Хендлер обратной связи - картинка
@dp.message_handler(content_types=ContentType.PHOTO)
async def cmd_message_photo(message: types.Message):
# распарсим ответ и записываем сообщение в базу данных
    text = message['caption']
    user_id = message['from']['id']
    message_id = message['message_id']
    photo = os.path.join('images', message.photo[-1].file_unique_id + '.jpg')
    await message.photo[-1].download(destination_file=photo)
#cохраняем данные в базу данных
    await save_message(text, user_id, message_id, photo, file=None)
# Отвечаем пользователю
    await message.answer(text='Спасибо за обратную связь\n Ваше сообщение сохранено', reply_markup=sign_inup_kb.markup)
#пересылаем сообщение администратору
    if user_id != ADMIN_ID:
        await bot.forward_message(chat_id=ADMIN_ID, from_chat_id=user_id, message_id=message_id)


#Хендлер обратной связи - видео
@dp.message_handler(content_types=ContentType.VIDEO)
async def cmd_message_video(message: types.Message):
#парсим сообщение и записываем в базу данных
    text = message['caption']
    user_id = message['from']['id']
    message_id = message['message_id']
    video = os.path.join('upload', message.video.file_unique_id + '.mp4')
    await message.video.download(destination_file=video)
# Отвечаем пользователю
    await message.answer(text='Спасибо за обратную связь\n Ваше сообщение сохранено', reply_markup=sign_inup_kb.markup)
#пересылаем сообщение администратору
    if user_id != ADMIN_ID:
        await bot.forward_message(chat_id=ADMIN_ID, from_chat_id=user_id, message_id=message_id)
    await save_message(text, user_id, message_id, photo=None, file=video)


#Хендлер обратной связи - документ
@dp.message_handler(content_types=ContentType.ANY)
async def cmd_message_document(message: types.Message):
    #парсим сообщение и записываем в базу данных
    text = message['caption']
    user_id = message['from']['id']
    message_id = message['message_id']
    if document := message.document:
        await document.download(destination_file=f'upload/{document.file_name}')
    document_name = f'upload/{document.file_name}'
    await save_message(text, user_id, message_id, photo=None, file=document_name)
# Отвечаем пользователю
    await message.answer(text='Спасибо за обратную связь\n Ваше сообщение сохранено', reply_markup=sign_inup_kb.markup)
#пересылаем сообщение администратору
    if user_id != ADMIN_ID:
        await bot.forward_message(chat_id=ADMIN_ID, from_chat_id=user_id, message_id=message_id)
"""""
# Сделан хендлер авторизации
new_user = {}
sign_in = {'current_state': False}
update_data = {}

REGISTRATION_TEXT = """
#Для регистрации сначала напишите свой логин!

#Из чего должен состоять логин?
#    - Логин должен состоять только из <b>латинских букв</b>!
 #   - Длинна логина должна быть <b>больше 3 символов(букв и цифр)</b>
#    - Логин должен быть <b>уникальным и не повторяющимися</b>

#Перед тем как отрпавить логин перепроверьте его!
#HELP_TEXT = """
#Привет 👋, я бот по продаже различных товаров! У нас есть такие команды как:

#<b>Помощь ⭐️</b> - помощь по командам бота
#<b>Описание 📌</> - адрес, контактные данные, график работы
#<b>Каталог 🛒</b> - список товаров которые можно купить
#<b>Админ 👑</b> - меню администратора

#Но перед началом нужно <b>зарегистрироваться или войти</b> в свой профиль.
#Нажми на команду <b>Регистрация ✌️'</b> или <b>Войти 👋</b>
#Если этого не сделаете, некоторые команды будут <b>не доступны</b> 🔴

#Рады что вы используете данного бота ❤️
"""


# Сделан дефолтный хендлер
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="Привет ✋, я бот по продаже различных товаров!\n\n"
                                    "У меня вы можете купить все что захотите, чтобы увидеть список "
                                    "товаров которые у меня есть.\n\n"
                                    "Нажмите снизу на команду 'Каталог 🛒'\n\n"
                                    "Но для начала <b>нужно зарегистрироваться</b>, "
                                    "иначе остальные команды будут не доступны!\n\n"
                                    "Нажми на команду <b>Регистрация ✌️'</b> или <b>Войти 👋</b>",
                               reply_markup=sign_inup_kb.markup)
    except:
        await message.reply(text="Чтобы можно было общаться с ботом, "
                                 "ты можешь написать мне в личные сообщение: "
                                 "https://t.me/yourbot")


@dp.message_handler(Text(equals='Помощь ⭐️'))
async def cmd_help(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=HELP_TEXT, reply_markup=default_kb.markup)


@dp.message_handler(Text(equals='Описание 📌'))
async def cmd_description(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="Привет ✋, мы компания по продаже различных товаров!, "
                                "Мы очень рады что Вы используете"
                                "наш сервис ❤️, мы работает с Понедельника до "
                                "Пятницы.\n9:00 - 21:00")
    await bot.send_location(chat_id=message.chat.id,
                            latitude=randrange(1, 100),
                            longitude=randrange(1, 100))


@dp.message_handler(Text(contains='Рассылка:'))
async def send_all(message: types.Message):
    if sign_in['current_state']:
        if message.chat.id == settings.ADMIN_ID:
            await message.answer(f"Сообщение: <b>{message.text[message.text.find(' '):]}</b> отправляется")
            async for user in User.objects.filter(is_registered=True):
                await bot.send_message(chat_id=user.chat_id, text=message.text[message.text.find(' '):])
            await message.answer("Все успешно отправлено!")
        else:
            await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


@dp.message_handler(Text(equals='Админ 👑'))
async def cmd_admin(message: types.Message):
    if sign_in['current_state']:
        if message.chat.id == settings.ADMIN_ID:
            await message.answer("Вы вошли в меню администратора 🤴\n\n"
                                 "Ниже предоставлены команды которые вы можете использовать 💭",
                                 reply_markup=admin_kb.markup)
        else:
            await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


@dp.message_handler(Text(equals='Домой 🏠'))
async def cmd_home(message: types.Message):
    if sign_in['current_state']:
        if message.chat.id == settings.ADMIN_ID:
            await message.answer("Вы успешно перешли в главное меню!", reply_markup=default_kb.markup)
        else:
            await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


HELP_ADMIN_TEXT = '''
Привет администратор 🙋\n\n
На данный момент у тебя есть такие команды как:
- <b>Рассылка:</b> - благодаря этой команде ты можешь отправить сообщение всем пользователями данного бота.
Пример использования: Рассылка: 'ТЕКСТ РАССЫЛКИ'
'''


@dp.message_handler(Text(equals='Помощь 🔔'))
async def cmd_help_admin(message: types.Message):
    if sign_in['current_state']:
        if message.chat.id == settings.ADMIN_ID:
            await message.answer(text=HELP_ADMIN_TEXT, reply_markup=admin_kb.markup)
        else:
            await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)



"""

def default_handlers_register():
 #   dp.register_message_handler(cmd_start, commands='start')
#    dp.register_message_handler(cmd_help, Text(equals='Помощь ⭐️'))
#    dp.register_message_handler(cmd_description, Text(equals='Описание 📌'))
#    dp.register_message_handler(send_all, Text(contains='Рассылка:'))
#    dp.register_message_handler(cmd_admin, Text(equals='Админ 👑'))
 # #  dp.register_message_handler(cmd_home, Text(equals='Домой 🏠'))
#    dp.register_message_handler(cmd_help_admin, Text(equals='Помощь 🔔'))
    dp.register_message_handler(cmd_message, Text(contains='Ф'))
    dp.register_message_handler(cmd_message_photo(content_types=ContentType.PHOTO))
    dp.register_message_handler(cmd_message_video(content_types=ContentType.VIDEO))
    dp.register_message_handler(cmd_message_document(content_types=ContentType.ANY))




"""
def authorization_handlers_register():
    dp.register_message_handler(command_cancel, Text(equals='Отмена ❌', ignore_case=True), state='*')
    dp.register_message_handler(process_registration, Text(equals='Регистрация ✌️'), state='*')
    dp.register_message_handler(process_login, state=AuthState.user_login)
    dp.register_message_handler(process_password, state=AuthState.user_password)
    dp.register_message_handler(process_password_2, state=AuthState.user_password_2)
    dp.register_message_handler(forgot_password, Text(equals='Забыли пароль? 🆘'), state='*')
    dp.register_message_handler(process_forgot_password_login, state=ForgotPasswordState.user_login)
    dp.register_message_handler(process_forgot_password_password, state=ForgotPasswordState.user_password)
    dp.register_message_handler(process_forgot_password_password_2, state=ForgotPasswordState.user_password_2)
    dp.register_message_handler(command_sign_in, Text(equals='Войти 👋'))
    dp.register_message_handler(process_sign_in, state=SignInState.login)
    dp.register_message_handler(process_pass, state=SignInState.password)
"""


#запускаем поллинг
def start_polling():
    executor.start_polling(dp, skip_updates=True)