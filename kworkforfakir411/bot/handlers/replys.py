from kworkforfakir411.settings import BOT_TOKEN
import requests

#Boзникла ошибка из-за изначальной несовместимости фреймворков, синхронного и асинхронного.
#Админка джанго синхронная, отправить сообщение из нее в аиограм невозможно.
#Отправляем сообщение кустарным методом
def send_reply_message(chat_id, message_id, text):
    return requests.get(
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}&reply_to_message_id={message_id}'
    )

def send_reply_photo(chat_id, message_id, text, photo):
    return requests.get(
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&text={text}&reply_to_message_id={message_id}&photo={photo}'
    )