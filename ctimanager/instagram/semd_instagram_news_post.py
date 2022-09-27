from mailgun2 import Mailgun
import datetime
import os

BASE_PATH = os.getcwd()
image_7h = "https://cryptapi-news-images.ams3.digitaloceanspaces.com/insta_gainers_losers_7d.png"
image_24h = "https://cryptapi-news-images.ams3.digitaloceanspaces.com/insta_gainers_losers_24h.png"
image_trending = "https://cryptapi-news-images.ams3.digitaloceanspaces.com/insta_top_trending.png"

try:
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mailer = Mailgun('alerts.toolsofthetrade.pro',os.environ.get('MAILGUN_PRIVATE_KEY'), os.environ.get('MAILGUN_PUBLIC_KEY'))
    mailer.send_message(from_email='instagram@alerts.toolsofthetrade.pro',
                        to='mail@barrydaniels.nl',
                        subject='Crypto Trade Ideas Story Posts',
                        html=f'<html><body><div><h1>Story Images for @crypto.trade.ideas for {date}</h1></div><br/><div style="float:left;margin-right:10px;"><img src="{image_trending}" width="300"></div><div style="float:left;margin-right:10px;"><img src="{image_7h}" width="300"></div><div style="float:left;margin-right:10px;"><img src="{image_24h}" width="300"></div></body></html>')
    print(mailer.get_events())
except Exception as e:
    print(f"Error with message {e}")

