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
project_root = "../../"
os.environ.get("DJANGO_SETTINGS_MODULE", "ctimanager.settings")
sys.path.append(project_path)
os.chdir(project_path)
import django
django.setup()
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
from webdriver_manager.utils import ChromeType
from urllib.parse import urlparse, parse_qs
import feedparser
from bs4 import BeautifulSoup, Comment
import pytz
from time import mktime
from datetime import datetime, timezone
from io import BytesIO
import boto3

SPACES_APIKEY = os.environ.get('SPACES_APIKEY')
SPACES_APISECRET = os.environ.get('SPACES_APISECRET')


from content.models import *

def main(): 
    """ Get sources and check feeds for new articles.. """
    sources = get_sources() 
    for source in sources:        
        get_new_articles(source)
        

def get_sources():
    return NewsSources.objects.filter(manual_import=True)

def get_full_article(link,selector,id):
    """ Get the full article text from the source """

    if selector.find('#ID#'):
        selector = selector.replace('#ID#',str(id))

    full_article_data = requests.get(link)    
    full_article_soup = BeautifulSoup(full_article_data.text,'html.parser')
    full_article_text = full_article_soup.select(selector)
    
    return clean_data(str(full_article_text))


def clean_data(source):
    """ Remove HTML and links from text """
    dirty_data = BeautifulSoup(source,'html.parser')
    almost_clean = dirty_data.get_text()
    clean = almost_clean.encode('ascii','ignore').decode("utf8")
    cleaner = clean.replace('\\n',' ')
    cleanest = cleaner.replace('\\xa0','')
    done1 = cleanest.replace('\U0001f4f0','')
    done2 = done1.replace('[','')
    done3 = done2.replace(']','')
    done4 = done3.replace('\U0001f525','')
    done5 = done4.replace('\\x','')
    done6 = done5.replace('\\t','')
    done7 = done6.replace('(adsbygoogle = window.adsbygoogle || ).push({});','')
    done8 = done7.replace('googletag.cmd.push(function() { googletag.display(\'div-gpt-ad-1567516716894-0\'); });','')
    return done8

def get_article_image(article_url):

    url = f"https://metafetcher.gurustacks.com/website/{article_url}"
    response = requests.get(url)
    response_json = response.json()
    try:
        image_url = response_json['images']['image']
        return image_url
    except Exception as e:
        print(f"Failed getting image with json: {response.json()}")


def get_new_articles(source):

    """ Get the feeds for a specific news source """      
    article = {}

    
    if source.rss_url.startswith('http'):    
        rss_data = requests.get(source.rss_url)
        feed_data = feedparser.parse(rss_data.text)
    
        for entries in feed_data['entries']:

            if 'link' in entries:
                if News.objects.filter(article_url=entries['link'],source=source).exists():
                    print(f"Link {entries['link']} already in database")
                else:
                    print(f"[get_new_articles] Getting link data for {entries['link']}")
                    try:
                        description = BeautifulSoup(entries['summary'],'html.parser')
                        article.update({'news_sources_id': source.id})
                        article.update({'excerpt': clean_data(description.get_text())})
                        article.update({'title': entries['title']})
                        article.update({'link': entries['link']})
                        article.update({'id_link': entries['id']})
                        article.update({'image': get_article_image(entries['link'])})

                        if(entries['link']!=entries['id']):
                            parsed = urlparse(entries['id'])
                            link_id = parse_qs(parsed.query)['p']
                            article.update({'id': link_id[0]})
                        else:
                            article.update({'id': 0})
        
                        article.update({'publish_date': datetime.fromtimestamp(mktime(entries['published_parsed']),pytz.UTC)})
                        article.update({'status': 'RECEIVED'})
                        article.update({'type': 'news'})
                        article.update({'full_article': get_full_article(entries['link'],source.article_selector,source.article_selector_id)})
                        add_article(article)
                    except Exception as e:
                        print(f"[get_new_article] Failed adding data for link: {entries['link']} with error: {e}")
                        
            else:
                print("[get_new_article] No links found for source.name ")
                print(entries)
    

def add_article(article):
    """ Add Articles """
    try:
        news_source = NewsSources.objects.get(pk=article['news_sources_id'])
        news = News.objects.create(source=news_source, type=article['type'], image=article['image'], article_url=article['link'], title=article['title'], excerpt=article['excerpt'], full_article=article['full_article'], published_at=article['publish_date'],status=article['status'])
        print(f"[add_article] Adding article {article['title']} to database")
    except Exception as e:
        print(f"[add_article] Failed adding news article with error: {e}")
    

main()



