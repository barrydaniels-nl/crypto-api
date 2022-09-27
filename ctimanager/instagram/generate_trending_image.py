import sys
sys.dont_write_bytecode = True

# Django specific settings
import os

project_path = "../"

sys.path.append(project_path)
os.chdir(project_path)
print(os.getcwd())
HOSTNAME = os.environ.get("HOSTNAME", "https://cryptapi-cc2no.ondigitalocean.app")

############################################################################
## START OF APPLICATION
############################################################################
import requests
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from datetime import datetime, timezone
import pytz
from time import sleep
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
def get_stats():

    try:
        url = "https://api.coingecko.com/api/v3/search/trending"
        response = requests.get(url)
        data = response.json()

        return data    
    except Exception as e:
        print(f"Error getting trending data with error: {e}")

def calculate_spaces(price):
    spaces_string = ""
    price = str(round(price,2))
    price = price.replace(".", "").replace("-", "")
    price_len = len(price)
    spaces = 5 - price_len
    for space in range(spaces):
        spaces_string = " " + spaces_string
    return spaces_string

def generate_trending():

        trending_data = get_stats()

        try:
            image_name = f"instagram/templates/insta_top_trending.png"
            template_image = Image.open(image_name)
        except FileNotFoundError as e:
            print(f"Template image not found {e}")
        
        try:
            project_font = ImageFont.truetype(f"instagram/fonts/Aileron-Regular.otf", 64)
            symbol_font = ImageFont.truetype(f"instagram/fonts/Aileron-Light.otf", 20)
            percentage_font = ImageFont.truetype(f"instagram/fonts/Aileron-Regular.otf", 64)
            footer_font = ImageFont.truetype(f"instagram/fonts/Aileron-Bold.otf", 24)
            date_font = ImageFont.truetype(f"instagram/fonts/Aileron-Regular.otf", 24)
        except Exception as e:
            print(f"Fonts not found {e}")

        publish_date = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")

        for i in range(0,len(trending_data['coins'])):
            url = f"{HOSTNAME}/api/prices?coingecko_id={trending_data['coins'][i]['item']['id']}"
            response = requests.get(url)
            data = response.json()
            
            name = data['prices_list'][0]['name']
            
            spaces = calculate_spaces(data['prices_list'][0]['price_change_percent_24h'])

            if data['prices_list'][0]['price_change_percent_24h'] > 0:
                percentage = spaces + "+" + str(round(data['prices_list'][0]['price_change_percent_24h'],2)) + " %"
            else:
                percentage = spaces + str(round(data['prices_list'][0]['price_change_percent_24h'],2)) + " %"
            
            img_response = requests.get(data['prices_list'][0]['image'])
            logo_image = Image.open(BytesIO(img_response.content)).resize((100, 100))
            template_image.convert('RGBA')
            template_image.paste(logo_image, (60, (348 + (i * 230))), logo_image.convert('RGBA'))                            
    
            draw = ImageDraw.Draw(template_image)
            if i==0: 
                draw.text((215, 357), name, font=project_font, fill=(210, 210, 210))
                if data['prices_list'][0]['price_change_percent_24h']>0:
                    draw.text((750, 357), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((750, 357), str(percentage), font=percentage_font, fill=(246, 88, 88))
            
            if i==1:
                draw.text((215, 584), name, font=project_font, fill=(210, 210, 210))
                if data['prices_list'][0]['price_change_percent_24h']>0:
                    draw.text((750, 584), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((750, 584), str(percentage), font=percentage_font, fill=(246, 88, 88))

            if i==2:
                draw.text((215, 810), name, font=project_font, fill=(210, 210, 210))
                if data['prices_list'][0]['price_change_percent_24h']>0:
                    draw.text((750, 810), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((750, 810), str(percentage), font=percentage_font, fill=(246, 88, 88))

            if i==3:
                draw.text((215, 1050), name, font=project_font, fill=(210, 210, 210))
                if data['prices_list'][0]['price_change_percent_24h']>0:
                    draw.text((750, 1050), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((750, 1050), str(percentage), font=percentage_font, fill=(246, 88, 88))

            if i==4:
                draw.text((215, 1280), name, font=project_font, fill=(210, 210, 210))
                if data['prices_list'][0]['price_change_percent_24h']>0:
                    draw.text((750, 1280), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((750, 1280), str(percentage), font=percentage_font, fill=(246, 88, 88))

            if i==5:
                draw.text((215, 1510), name, font=project_font, fill=(210, 210, 210))
                if data['prices_list'][0]['price_change_percent_24h']>0:
                    draw.text((750, 1510), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((750, 1510), str(percentage), font=percentage_font, fill=(246, 88, 88))

            if i==6:
                draw.text((215, 1740), name, font=project_font, fill=(210, 210, 210))
                if data['prices_list'][0]['price_change_percent_24h']>0:
                    draw.text((750, 1740), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((750, 1740), str(percentage), font=percentage_font, fill=(246, 88, 88))


        #draw.text((22, 446), "@crypto.trade.ideas", font=footer_font, fill=(255, 255, 255))
        draw.text((671, 1870), f"{publish_date} UTC", font=date_font, fill=(135, 168, 160))
            
        
        print(f"Generating trending image...")
        template_image.save(f"instagram/generated_images/insta_top_trending.png")
        print(f"Generating trending image...done")
   
        if upload_image_to_s3(f"instagram/generated_images/insta_top_trending.png","insta_top_trending.png"):
            print(f"Uploaded trending image to S3")
        else:
            print(f"Error uploading trending image to S3")


generate_trending()
