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
import time

# Import your models for use in your script
from content.models import News, Project, Prices

API_ID = os.environ.get('TELEGRAM_API_ID')
API_HASH = os.environ.get('TELEGRAM_API_HASH')
PHONE = os.environ.get('TELEGRAM_PHONE')
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

def publish_stats():

    client = TelegramClient('my_session', API_ID, API_HASH)
    client.connect()
    
    if not client.is_user_authorized():
        client.send_code_request(PHONE)
        # signing in the client
        client.sign_in(PHONE, input('Enter the telegram auth code: '))

    
    images = [f'https://cryptapi-news-images.ams3.digitaloceanspaces.com/gainers_1h_100.png?timestamp={time.time()}.png',
              f'https://cryptapi-news-images.ams3.digitaloceanspaces.com/gainers_24h_100.png?timestamp={time.time()}.png',
              f'https://cryptapi-news-images.ams3.digitaloceanspaces.com/gainers_7d_100.png?timestamp={time.time()}.png',
              f'https://cryptapi-news-images.ams3.digitaloceanspaces.com/losers_1h_100.png?timestamp={time.time()}.png',
              f'https://cryptapi-news-images.ams3.digitaloceanspaces.com/losers_24h_100.png?timestamp={time.time()}.png',
              f'https://cryptapi-news-images.ams3.digitaloceanspaces.com/losers_7d_100.png?timestamp={time.time()}.png',
              f'https://cryptapi-news-images.ams3.digitaloceanspaces.com/trending.png?timestamp={time.time()}.png',
              f'https://cryptapi-news-images.ams3.digitaloceanspaces.com/volume_increase_100.png?timestamp={time.time()}.png',
              f'https://cryptapi-news-images.ams3.digitaloceanspaces.com/volume_decrease_100.png?timestamp={time.time()}.png']
    

    
    for message_image in images:
        client.send_file(entity="@cryptonewscasters", file=message_image)
        time.sleep(1)
        
    client.disconnect()    

if __name__ == '__main__':
    publish_stats()
