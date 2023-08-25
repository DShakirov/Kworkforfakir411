import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kworkforfakir411.settings')
django.setup()

from bot.handlers.dispatcher import start_polling

if __name__ == '__main__':
    print('Polling started')
    start_polling()
