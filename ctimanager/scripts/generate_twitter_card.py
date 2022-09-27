############################################################################
## Django ORM Standalone Python Template
############################################################################

# Turn off bytecode generation
from datetime import time
import sys
sys.dont_write_bytecode = True
import platform

# Django specific settings
import os
project_path = "../"
os.environ.get("DJANGO_SETTINGS_MODULE", "ctimanager.settings")
sys.path.append(project_path)
os.chdir(project_path)
import django
django.setup()

# Import your models for use in your script
from content.models import *

############################################################################
## START OF APPLICATION
############################################################################
import requests
import json 
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs
from PIL import Image, ImageChops, ImageDraw2, ImageFont
from io import BytesIO
import random
import boto3
import platform

SPACES_APIKEY = os.environ.get('SPACES_APIKEY')
SPACES_APISECRET = os.environ.get('SPACES_APISECRET')

def generate_tweet(url,news_id):
    url = f"https://publish.twitter.com/oembed?url={url}"
    response = requests.get(url)
    
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document</title>
        <style>
            blockquote {{ margin: 0; padding: 0; }}
            iframe {{ margin: 0px; padding: 0px; }}
        </style>
    </head>
    <body style="padding:0px;margin:0px;">
        <div id="tweet" style="display:inline-block;padding:0px;margin:0px;">
            {response.json()['html']}
        </div>
    </body>
    </html>
    '''
    file = open(f"scripts/tweet_files/tweet_{news_id}.html", "w")
    file.write(html)
    file.close()


def upload_image_to_s3(image_url, image_name):
    try:        
        session = boto3.session.Session()
        client = session.client('s3', region_name='ams3',
                                endpoint_url='https://ams3.digitaloceanspaces.com',
                                aws_access_key_id=SPACES_APIKEY,
                                aws_secret_access_key=SPACES_APISECRET)

        client.upload_file(image_url, 'cryptapi-news-images', image_name, ExtraArgs={'ACL':'public-read'})
        return True

    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

def remote_file_exists(url):
    try:
        r = requests.head(url)
        return r.status_code == requests.codes.ok
    except:
        return False

for news in News.objects.filter(telegram_status='WAITING').order_by('-published_at'):
    
    try:
        if "@" in news.domain:
            
            try:
                generate_tweet(news.article_url,news.id)
            except Exception as e:
                print(f"Error generating tweet: {e}")
                continue
            
            file_path = f"{os.getcwd()}/../static/content/media/twitter_card_{news.id}.png"
            
            """
            if platform.system() == "Linux":
                file_path = f"/home/cryptapi/cryptapi/static/content/media/twitter_card_{news.id}.png" 
            else:
                file_path = f"{os.getcwd()}/static/content/media/twitter_card_{news.id}.png"
            """

            if not os.path.exists(file_path):
        
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-gpu")
                    
                os.environ['WDM_LOG_LEVEL'] = '0'
                os.environ['WDM_PRINT_FIRST_LINE'] = 'False'
                
                try:
                    if platform.system() == "Linux":
                        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)
                    else:
                        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

                    filename = f"{os.getcwd()}/scripts/tweet_files/tweet_{news.id}.html"
                    print(filename)
                    driver.get(f"file:///{filename}")
                    driver.set_window_size(3000,3000)
                    driver.execute_script("document.body.style.zoom='140%'")
                    time.sleep(3)
                    article = driver.find_element(By.ID, "tweet")
                    
                    time.sleep(3)
                    
                    article.screenshot(file_path)
                    driver.quit()

                    try:
                        upload_image_to_s3(file_path, f"twitter_card_{news.id}.png")
                        print(f"uploaded: {file_path} to S3")
                    except Exception as e:
                        print(f"Error uploading file: {e} to S3")

                except Exception as e:
                    print(f"Error: {e}")
                    continue
                

    except Exception as e:
        print(f"Error reading image with error: {e}")
    