import sys
sys.dont_write_bytecode = True

# Django specific settings
import os

project_path = "../../"

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

    url = "https://api.coingecko.com/api/v3/search/trending"
    response = requests.get(url)
    data = response.json()
    return data    

def generate_trending():
    
        image_design_type = "straight"

        trending_data = get_stats()
        image_name = f"telegram_bot/scripts/templates/{image_design_type}/trending.png"

        template_image = Image.open(image_name)
        
        project_font = ImageFont.truetype("telegram_bot/scripts/fonts/Aileron-Regular.otf", 30)
        symbol_font = ImageFont.truetype("telegram_bot/scripts/fonts/Aileron-Light.otf", 20)
        percentage_font = ImageFont.truetype("telegram_bot/scripts/fonts/Aileron-Regular.otf", 30)
        footer_font = ImageFont.truetype("telegram_bot/scripts/fonts/Aileron-Bold.otf", 25)
        date_font = ImageFont.truetype("telegram_bot/scripts/fonts/Aileron-Regular.otf", 25)
        
        publish_date = datetime.now(timezone.utc).strftime("%m/%d/%Y %H:%M")
    
        for i in range(0,5):
            url = f"{HOSTNAME}/api/prices?coingecko_id={trending_data['coins'][i]['item']['id']}"
            response = requests.get(url)
            data = response.json()
            
            price = data['prices_list'][0]['volume_change_percent_24h']
            name = data['prices_list'][0]['name']

            
            if data['prices_list'][0]['price_change_percent_1h'] > 0:
                percentage = "+" + str(round(data['prices_list'][0]['price_change_percent_1h'],2)) + "%"
            else:
                percentage = str(round(data['prices_list'][0]['price_change_percent_1h'])) + "%"
            
            img_response = requests.get(data['prices_list'][0]['image'])
            logo_image = Image.open(BytesIO(img_response.content)).resize((40, 40))
            template_image.convert('RGBA')
            template_image.paste(logo_image, (72, (82 + (i * 70))), logo_image.convert('RGBA'))                            
            # add text
            draw = ImageDraw.Draw(template_image)
            if i==0: 
                draw.text((138, 82), name, font=project_font, fill=(88, 88, 88))
                if data['prices_list'][0]['price_change_percent_1h']>0:
                    draw.text((460, 82), str(percentage), font=percentage_font, fill=(68, 127, 51))
                else:
                    draw.text((460, 82), str(percentage), font=percentage_font, fill=(127, 51, 51))
            
            if i==1:
                draw.text((138, 152), name, font=project_font, fill=(88, 88, 88))
                if data['prices_list'][0]['price_change_percent_1h']>0:
                    draw.text((460, 152), str(percentage), font=percentage_font, fill=(68, 127, 51))
                else:
                    draw.text((460, 152), str(percentage), font=percentage_font, fill=(127, 51, 51))

            if i==2:
                draw.text((138, 225), name, font=project_font, fill=(88, 88, 88))
                if data['prices_list'][0]['price_change_percent_1h']>0:
                    draw.text((460, 225), str(percentage), font=percentage_font, fill=(68, 127, 51))
                else:
                    draw.text((460, 225), str(percentage), font=percentage_font, fill=(127, 51, 51))

            if i==3:
                draw.text((138, 295), name, font=project_font, fill=(88, 88, 88))
                if data['prices_list'][0]['price_change_percent_1h']>0:
                    draw.text((460, 295), str(percentage), font=percentage_font, fill=(68, 127, 51))
                else:
                    draw.text((460, 295), str(percentage), font=percentage_font, fill=(127, 51, 51))
            if i==4:
                draw.text((138, 358), name, font=project_font, fill=(88, 88, 88))
                if data['prices_list'][0]['price_change_percent_1h']>0:
                    draw.text((460, 358), str(percentage), font=percentage_font, fill=(68, 127, 51))
                else:
                    draw.text((460, 358), str(percentage), font=percentage_font, fill=(127, 51, 51))

        draw.text((22, 446), "@cryptonewscasters", font=footer_font, fill=(255, 255, 255))
        draw.text((349, 448), f"{publish_date} UTC", font=date_font, fill=(135, 168, 160))
            
        
        print(f"Generating trending image...")
        template_image.save(f"telegram_bot/generated_images/trending.png")
        if upload_image_to_s3(f"telegram_bot/generated_images/trending.png","trending.png"):
            print(f"Uploaded trending image to S3")
        else:
            print(f"Error uploading trending image to S3")

sleep(40)
generate_trending()
