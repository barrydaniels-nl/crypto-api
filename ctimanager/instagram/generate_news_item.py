import json
import requests
from playwright.sync_api import sync_playwright
import datetime
import os
import sys
import boto3


HOSTNAME = os.environ.get("HOSTNAME", "https://cryptapi-cc2no.ondigitalocean.app")
SPACES_APIKEY = os.environ.get('SPACES_APIKEY')
SPACES_APISECRET = os.environ.get('SPACES_APISECRET')

class CreateNewsItems:

    def __init__(self):
        self.news = self.get_news()
        self.create_news_items()

    def get_news(self):
        api_url = "http://127.0.0.1:8000/api/topnews"
        data = requests.get(api_url).json()['object_list']
        return data

    def write_log(self,url):
        with open('log.txt', 'a') as f:
            f.write(url + '\n')

    def upload_image_to_s3(self, image_url, image_name):

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

    def create_news_items(self):
        
        with open('log.txt', 'r') as f:
            log = f.read().split('\n')

        for news_item in self.news:
            if news_item['article_url'] not in log:
                print(f"Generating news item for {news_item['article_url']}")
                published_date = datetime.datetime.strptime(news_item['published_at'], '%Y-%m-%d %H:%M:%S.%f%z')
                # Wednesday, March 5, 2022, 13:32 UTC
                date = published_date.strftime("%A, %B %d, %Y, %H:%M UTC")
                url = f"http://127.0.0.1:8000/static/templates/newspost/index.html?title={news_item['title']}&image={news_item['image']}&projects={','.join(news_item['projects'])}&published={date}"
                with sync_playwright() as p:
                    browser = p.webkit.launch()
                    context = browser.new_context(viewport={"width": 1080, "height": 1920})
                    page = context.new_page()
                    page.goto(url)
                    page.wait_for_load_state("networkidle")
                    page.screenshot(path=f"screenshots/news_post_{news_item['id']}.png")
                    page.close()
                    browser.close() 
                    
                    try:
                        self.upload_image_to_s3(f"screenshots/news_post_{news_item['id']}.png", f"news_post_{news_item['id']}.png")
                        print(f"Uploaded news-item {news_item['id']} to S3")
                    except Exception as e:
                        print(f"Failed to upload image: {e}")


                    self.write_log(news_item['article_url'])
                

if __name__ == "__main__":
    CreateNewsItems()