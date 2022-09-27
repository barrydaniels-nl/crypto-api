from cgitb import html
from html.entities import html5
from mailgun2 import Mailgun
import datetime
import os

from prompt_toolkit import HTML

DOMAIN = "alerts.toolsofthetrade.pro"
PUBLIC_KEY = os.environ.get('MAILGUN_PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('MAILGUN_PRIVATE_KEY')

class SendImages:

    def __init__(self) -> None:
        pass

    def send_images(self, images: list, subject: str, to: str, header: str) -> None:

        image_7h = "https://cryptapi-news-images.ams3.digitaloceanspaces.com/insta_gainers_losers_7d.png"
        image_24h = "https://cryptapi-news-images.ams3.digitaloceanspaces.com/insta_gainers_losers_24h.png"
        image_trending = "https://cryptapi-news-images.ams3.digitaloceanspaces.com/insta_top_trending.png"

        try:
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mailer = Mailgun(DOMAIN, PRIVATE_KEY, PUBLIC_KEY)
            
            for image in images:
                image_html += f'<div style="float:left;margin-right:10px;"><img src="{image}" width="300"></div>'

            html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    {image_html}
</body>
</html>            
            """
            mailer.send_message(from_email='crypto-trade-alerts@alerts.toolsofthetrade.pro',
                                to=to,
                                subject=subject,
                                html=f'<html><body><div><h1>{header}</h1></div><br/><div style="float:left;margin-right:10px;"><img src="{image_trending}" width="300"></div><div style="float:left;margin-right:10px;"><img src="{image_7h}" width="300"></div><div style="float:left;margin-right:10px;"><img src="{image_24h}" width="300"></div></body></html>')
            return mailer.get_events()
        except Exception as e:
            print(f"Error with message {e}")


if __name__ == "__main__":
    SendImages()