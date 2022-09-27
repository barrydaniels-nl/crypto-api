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
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from urllib.parse import urlparse, parse_qs
from PIL import Image, ImageChops, ImageDraw2, ImageFont
from io import BytesIO
import boto3

SPACES_APIKEY = os.environ.get('SPACES_APIKEY')
SPACES_APISECRET = os.environ.get('SPACES_APISECRET')


"""
class NewsSources(models.Model):
    name = models.CharField(max_length=100, blank=True)
    title = models.TextField(blank=False)
    domain = models.CharField(max_length=100, blank=False)
    rss_url = models.URLField()
    article_selector = models.CharField(max_length=255)
    region = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return self.name


class News(models.Model):
    cryptopanic_id = models.IntegerField(blank=True)
    cryptopanic_url = models.URLField(blank=True)
    type = models.CharField(max_length=20, blank=False)
    domain = models.CharField(max_length=100, blank=True, null=True)
    projects = models.ManyToManyField(Project)
    # Note! The JSON1 module needs to be enables in SQL, if you get an error this might be the problem. 
    votes = models.JSONField(blank=True, null=True)
    article_url = models.URLField(blank=False)
    source = models.ForeignKey(NewsSources, on_delete=models.SET_NULL, null=True)
    publish_data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name    

"""

def resize_and_store(news_id, image_url):

        try:
            if image_url:

                file_path = f"{BASE_PATH}/static/content/media/news_image_{news_id}.png"

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
                

                response = requests.get(image_url, proxies=proxies, headers=headers)

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
                    if upload_image_to_s3(file_path,f"news_image_{news_id}.png"):
                        print("image uploaded to s3")
                    else:
                        print("image not uploaded to s3")


                else:
                    print(f"Response code {response.status_code} message: {response.text}")


        except Exception as e:
            print(f"Error reading image with error: {e}")

def check_news_source(source):

    try:
        if NewsSources.objects.filter(title=source['title']).exists():
            return True
        else:
            try:
                title = source['title']
            except Exception as e:
                print("No title found for source {source}")

            try:
                domain = source['domain']
            except Exception as e:
                print("No domain found for source {source}")
            
            try:
                region = source['region']
            except Exception as e:
                print("No region found for source {source}")

            try:
                path = source['path']
            except Exception as e:
                print("No path found for source {source}")
   

            NewsSources.objects.create(domain=domain, region=region, title=title, path=path)
            return True
            
    except Exception as e:
        print(f"Trouble checking and adding the news source with error {e}")
        return False


def extract_video_id(url):

    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/watch/': return query.path.split('/')[1]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
        # below is optional for playlists
        if query.path[:9] == '/playlist': return parse_qs(query.query)['list'][0]
   # returns None for invalid YouTube url
    return None
    


def get_real_url(cryptopanic_url,source_domain):
    print(f"getting real url for cryptopanic_url: {cryptopanic_url}")

    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
    
    os.environ['WDM_LOG_LEVEL'] = '0'
    os.environ['WDM_PRINT_FIRST_LINE'] = 'False'

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument('--proxy-server=socks5://84.107.32.223:1080')
    chrome_options.add_argument(f"--user-agent={ua}")
    
    try:
        if sys.platform == "darwin":
            browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        else:
            browser = webdriver.Chrome(executable_path="chromedriver", options=chrome_options)
        
        browser.get(cryptopanic_url)
        time.sleep(3)
        url = browser.find_element(By.XPATH, '//*[@id="detail_pane"]/div[1]/h1/a[2]').get_attribute('href')
        print(f"article url: {url}")
        browser.quit()
        

        return url
    except Exception as e:
        print(f"error: {e}")



def get_article_image(article_url):

    if 'youtube.com' in article_url or 'youtu.be' in article_url:
        video_id = extract_video_id(article_url)
        url = f"https://metafetcher.gurustacks.com/video/youtube/{video_id}"

        response = requests.get(url)

        if response.status_code==200:
            if 'standard' in response.json()['images']:
                return response.json()['images']['standard']['url']
            else:
                return None
                
    elif 'twitter.com' in article_url:
        url = f"https://metafetcher.gurustacks.com/website/{article_url}"
        response = requests.get(url)

        if response.status_code==200:
            if 'icon_192x192' in response.json()['images']:
                return response.json()['images']['icon_192x192']
            else:
                return None

    else:
        url = f"https://metafetcher.gurustacks.com/website/{article_url}"
        response = requests.get(url)

        if response.status_code==200:
            if 'image' in response.json()['images']:
                return response.json()['images']['image']
            else:
                return None
    

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


for num in range(1,5):

    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={os.environ.get('CRYPTO_PANIC_API_KEY')}&page={num}"

    try:
        response = requests.get(url)

        if response.status_code==200:

            for item in response.json()['results']:
                
                if check_news_source(item['source']):    
                    cryptopanic_id = item['id']
                    
                    if item['source']['domain'] == 'twitter.com':
                        type = "twitter"
                    else:
                        type = item['kind']

                    title = item['title']
                    published_at = item['published_at']
                    cryptopanic_url = item['url']
                    votes = item['votes']
                    domain = item['domain']        
                    
                    try:
                        source_obj = NewsSources.objects.get(title=item['source']['title'])
                    except Exception as e:
                        print(f"News Source Not Found with error {e} for  {item}")

                    if News.objects.filter(cryptopanic_id=cryptopanic_id).exists():

                        try:
                            news = News.objects.get(cryptopanic_id=cryptopanic_id)

                            if news.article_url == "":
                                article_url = get_real_url(cryptopanic_url,item['source']['domain']) 
                                if article_url:
                                    news.article_url = article_url
                                else:
                                    news.delete()
                                    continue

                            news.votes = item['votes']
                            news.title = item['title']
                            news.save()
                            print(f"Updating news item {item['title']}")
                        except Exception as e:
                            print(f"Failed updating news item with error {e}")

                    else:
                        try:
                            article_url = get_real_url(cryptopanic_url,item['source']['domain']) 
                            if article_url is not None:
                                article_image = get_article_image(article_url)
                                
                                if article_image is not None:           
                                    news_item = News.objects.create(cryptopanic_id=cryptopanic_id, article_url=article_url, type=type, title=title, image=article_image, domain=domain, published_at=published_at, cryptopanic_url=cryptopanic_url, votes=votes, source=source_obj)
                                    print(f"Adding news item with title {title} and new news_id: {news_item.id}")

                                    # Resize and store imnage
                                    if article_image:
                                        try:
                                            resize_and_store(news_item.id, news_item.image)
                                        except Exception as e:
                                            print("Failed downloading image for news item")

                                    try:
                                        if 'currencies' in item.keys():
                                            for currency in item['currencies']:
                                                symbol = currency['code'].lower()
                                                if Project.objects.filter(symbol=symbol,status='ACTIVE').exists():
                                                    news_item.projects.add(Project.objects.filter(symbol=symbol,status='ACTIVE').first())
                                                    print(f"adding {symbol} to news item")
                                                else:
                                                    print(f"No project found for currency {symbol}")

                                    except Exception as e:
                                        print(f"Problems adding projects to news item with error {e}")
                                else:
                                    raise Exception(f"No image found for news item {item['url']}")

                            else:
                                raise Exception("Article URL not found")
                                
                        except Exception as e:
                            print(f"Failed adding news item with error {e}")
                else:
                    print(f"Problems with the news source.. Skipping..")
        
        else:
            print(f"Not Hotdog! {response.status_code}")
            time.sleep(5)

    except Exception as e:
        print("Time out! Skipping")