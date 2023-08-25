from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import check_password
from ..models import User, Message

@sync_to_async
def save_message(text, user_id, message_id, photo, file):
    Message.objects.create(
        message_id=message_id, text=text, user=User.objects.get(chat_id=user_id), image=photo, file=file
    )

@sync_to_async
def save_user():
    user = User.objects.create(user_login=new_user['user_login'],
                                       user_password=make_password(new_user['user_password']),
                                       is_registered=True,
                                       chat_id=new_user['chat_id'])
    return user

@sync_to_async
def update_user_password(login, password):
    user = User.objects.filter(user_login=login).update(user_password=make_password(password))
    return user

@sync_to_async
def get_password(username, password):
    user = User.objects.get(user_login=username)
    if check_password(password, user.user_password):
        return True
    else:
        return False

@sync_to_async
def check_user(login):
    return User.objects.filter(user_login=login).exists()

@sync_to_async
def check_login_chat_id(login, chat_id):
    return User.objects.filter(user_login=login, chat_id=chat_id).exists()

@sync_to_async
def check_users_chat_id(chat_id):
    return User.objects.filter(chat_id=chat_id).exists()



