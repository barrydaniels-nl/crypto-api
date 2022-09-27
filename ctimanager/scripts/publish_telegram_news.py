############################################################################
## Django ORM Standalone Python Template
############################################################################

# Turn off bytecode generation
from datetime import time
import sys
sys.dont_write_bytecode = True

# Django specific settings
import os
project_path = "../"
os.environ.get("DJANGO_SETTINGS_MODULE", "ctimanager.settings")
sys.path.append(project_path)
os.chdir(project_path)
import django
django.setup()

import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
from time import sleep

# Import your models for use in your script
from content.models import News, Project, Prices

API_ID = os.environ.get('TELEGRAM_API_ID')
API_HASH = os.environ.get('TELEGRAM_API_HASH')
PHONE = os.environ.get('TELEGRAM_PHONE')
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

def send_message(message):

    message_url = message['url']
    message_title = message['title']
    message_id = message['news_id']
    message_image = message['image']

    message_html = f'<html><body><table style="width: 100%;"><tr><td style="width: 100%;"><b><h1><a href="{message_url}">{message_title}</a></h1></b></td></tr></table></body></html>'

    client = TelegramClient('my_session', API_ID, API_HASH)
    client.connect()
    
    if not client.is_user_authorized():
        client.send_code_request(PHONE)
        # signing in the client
        client.sign_in(PHONE, input('Enter the telegram auth code: '))

    client.parse_mode = 'html'
    client.send_file(entity="@cryptonewscasters", file=message_image, caption=message_html)
    client.disconnect()

def send_tweet(message):

    message_url = message['url']
    message_title = message['title']
    message_id = message['news_id']
    message_image = message['image']

    message_html = f'<html><body><table style="width: 100%;"><tr><td style="width: 100%;"><b><h1><a href="{message_url}">Read on Twitter</a></h1></b></td></tr></table></body></html>'

    client = TelegramClient('my_session', API_ID, API_HASH)
    client.connect()
    
    if not client.is_user_authorized():
        client.send_code_request(PHONE)
        # signing in the client
        client.sign_in(PHONE, input('Enter the telegram auth code: '))

    tweet_image = f"https://cryptapi-news-images.ams3.digitaloceanspaces.com/twitter_card_{message['news_id']}.png"
    tweet_image = f"{os.getcwd()}/../static/content/media/twitter_card_{message['news_id']}.png"    
    client.send_file(entity="@cryptonewscasters", file=tweet_image, caption=message_html, parse_mode='html')
    client.disconnect()


def get_news_items():
    news_items = News.objects.filter(telegram_status='WAITING')

    for news_item in news_items:

        print(f"Sending news id: {news_item.id} to Telegram")
        
        message = {
            'title': news_item.title,
            'url': news_item.article_url,
            'news_id': news_item.id,
            'image': news_item.image,
            'domain': news_item.domain
        }

        try:
            if '@' in news_item.domain:
                send_tweet(message)
                news_item.telegram_status = 'PUBLISHED'
                news_item.save()
                sleep(2)
            else:
                send_message(message)
                news_item.telegram_status = 'PUBLISHED'
                news_item.save()
                sleep(2)
        except Exception as e:
            print(f"Failed sending message to telegram with error {e}")
            print(message)
            news_item.telegram_status = 'WAITING'
            news_item.save()
 

if __name__ == '__main__':
    get_news_items()


        