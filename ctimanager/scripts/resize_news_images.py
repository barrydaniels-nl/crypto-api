ktgglhrduuurjtbvg
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
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs
from PIL import Image, ImageChops, ImageDraw2, ImageFont
from io import BytesIO
import random
import boto3

SPACES_APIKEY = os.environ.get('SPACES_APIKEY')
SPACES_APISECRET = os.environ.get('SPACES_APISECRET')

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


for news in News.objects.all():
    
    try:
        if news.image:

            file_path = f"{os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}/static/content/media/news_image_{news.id}.png" 

            if not os.path.exists(file_path):

                proxies = {'http': "socks5://84.107.32.223:1080", 'https': "socks5://84.107.32.223:1080"}

                headers = {
                        "Connection": "keep-alive",
                        "DNT": "1",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Dest": "document",
                        "Referer": "https://www.google.com/",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8" }
                

                response = requests.get(news.image, proxies=proxies, headers=headers)

                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))

                    if img.height < 629:
                        myheight = 629
                        hpercent = (myheight/float(img.size[1]))
                        wsize = int((float(img.size[0])*float(hpercent)))
                        img = img.resize((wsize,myheight), resample=Image.ANTIALIAS)                


                    mywidth = 1200
                    
                    wpercent = (mywidth/float(img.size[0]))
                    hsize = int((float(img.size[1])*float(wpercent)))
                    img = img.resize((mywidth,hsize), resample=Image.ANTIALIAS)

                    new_width = 1200
                    new_height = 629

                    width, height = img.size   # Get dimensions

                    left = (width - new_width)/2
                    top = (height - new_height)/2
                    right = (width + new_width)/2
                    bottom = (height + new_height)/2

                    # Crop the center of the image
                    im = img.crop((left, top, right, bottom))

                    im.save(file_path, format="png")
            
                    print(f"saving: {file_path}")
                    
                    try:
                        upload_image_to_s3(file_path, f"news_image_{news.id}.png")
                        print(f"uploaded: {file_path} to S3")
                    except Exception as e:
                        print(f"Error uploading file: {e} to S3")


                else:
                    print(f"Response code {response.status_code} message: {response.text}")
            
            else:
                file_url = f"https://cryptapi-news-images.ams3.digitaloceanspaces.com/news_image_{news.id}.png"
                if remote_file_exists(file_url):
                    print(f"All Clear For: {file_url}")

        else:
            News.objects.get(id=news.id).delete()
            print(f"Deleted news: {news.id}")

    except Exception as e:
        print(f"Error reading image with error: {e}")
    