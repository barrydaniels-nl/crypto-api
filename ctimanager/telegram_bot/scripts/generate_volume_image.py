from PIL import Image, ImageFont, ImageDraw
import requests
from io import BytesIO
from datetime import datetime, timezone
import pytz
import os
import sys
from time import sleep
import boto3

project_path = "../../"
os.environ.get("DJANGO_SETTINGS_MODULE", "ctimanager.settings")
sys.path.append(project_path)
os.chdir(project_path)
HOSTNAME = os.environ.get("HOSTNAME", "https://cryptapi-cc2no.ondigitalocean.app")
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

def get_stats(type, limit):

    if type == "increase":
        url = f"{HOSTNAME}/api/prices/volume_increase/{limit}"
    elif type == "decrease":
        url = f"{HOSTNAME}/api/prices/volume_decrease/{limit}"
    print(url)
    response = requests.get(url)
    data = response.json()
    return data    

def generate_gain_lose_image(type, limit):

    if type == "increase" or type == "decrease":
        
        data = get_stats(type, limit)
        
        image_design_type = "straight"

        if type == "increase":
            image_name = f"telegram_bot/scripts/templates/{image_design_type}/volume_increase_24h.png"
        elif type == "decrease":
            image_name = f"telegram_bot/scripts/templates/{image_design_type}/volume_decrease_24h.png"

        template_image = Image.open(image_name)
        
        project_font = ImageFont.truetype("telegram_bot/scripts/fonts/Aileron-Regular.otf", 30)
        symbol_font = ImageFont.truetype("telegram_bot/scripts/fonts/Aileron-Light.otf", 20)
        percentage_font = ImageFont.truetype("telegram_bot/scripts/fonts/Aileron-Regular.otf", 30)
        footer_font = ImageFont.truetype("telegram_bot/scripts/fonts/Aileron-Bold.otf", 25)
        date_font = ImageFont.truetype("telegram_bot/scripts/fonts/Aileron-Regular.otf", 25)
        
        publish_date = datetime.now(timezone.utc).strftime("%m/%d/%Y %H:%M")
    
        for i in range(0,5):
            name = data['prices_list'][i]["name"]
            symbol = data['prices_list'][i]["symbol"]
            if data['prices_list'][i]["volume_change_percent_24h"] > 0:
                percentage = "+" + str(data['prices_list'][i]["volume_change_percent_24h"]) + "%"
            else:
                percentage = "-" + str(data['prices_list'][i]["volume_change_percent_24h"]) + "%"
            percentage = str(round(data['prices_list'][i]["volume_change_percent_24h"],2)) + " %"
            img_response = requests.get(data['prices_list'][i]["image"])
            logo_image = Image.open(BytesIO(img_response.content)).resize((40, 40))
            template_image.convert('RGBA')
            template_image.paste(logo_image, (72, (82 + (i * 70))), logo_image.convert('RGBA'))                            
            # add text
            draw = ImageDraw.Draw(template_image)
            if i==0: 
                draw.text((138, 82), name, font=project_font, fill=(88, 88, 88))
                if float(data['prices_list'][i]["volume_change_percent_24h"])>0:
                    draw.text((460, 82), str(percentage), font=percentage_font, fill=(68, 127, 51))
                else:
                    draw.text((460, 82), str(percentage), font=percentage_font, fill=(127, 51, 51))
            
            if i==1:
                draw.text((138, 152), name, font=project_font, fill=(88, 88, 88))
                if float(data['prices_list'][i]["volume_change_percent_24h"])>0:
                    draw.text((460, 152), str(percentage), font=percentage_font, fill=(68, 127, 51))
                else:
                    draw.text((460, 152), str(percentage), font=percentage_font, fill=(127, 51, 51))

            if i==2:
                draw.text((138, 225), name, font=project_font, fill=(88, 88, 88))
                if float(data['prices_list'][i]["volume_change_percent_24h"])>0:
                    draw.text((460, 225), str(percentage), font=percentage_font, fill=(68, 127, 51))
                else:
                    draw.text((460, 225), str(percentage), font=percentage_font, fill=(127, 51, 51))

            if i==3:
                draw.text((138, 295), name, font=project_font, fill=(88, 88, 88))
                if float(data['prices_list'][i]["volume_change_percent_24h"])>0:
                    draw.text((460, 295), str(percentage), font=percentage_font, fill=(68, 127, 51))
                else:
                    draw.text((460, 295), str(percentage), font=percentage_font, fill=(127, 51, 51))
            if i==4:
                draw.text((138, 358), name, font=project_font, fill=(88, 88, 88))
                if float(data['prices_list'][i]["volume_change_percent_24h"])>0:
                    draw.text((460, 358), str(percentage), font=percentage_font, fill=(68, 127, 51))
                else:
                    draw.text((460, 358), str(percentage), font=percentage_font, fill=(127, 51, 51))

        
        draw.text((22, 446), "@cryptonewscasters", font=footer_font, fill=(255, 255, 255))
        if type == "increase":
            draw.text((349, 448), f"{publish_date} UTC", font=date_font, fill=(135, 168, 160))
        elif type == "decrease":
            draw.text((349, 448), f"{publish_date} UTC", font=date_font, fill=(217, 143, 143))
        
        template_image.save(f"telegram_bot/generated_images/volume_{type}_{limit}.png")

        if upload_image_to_s3(f"telegram_bot/generated_images/volume_{type}_{limit}.png", f"volume_{type}_{limit}.png"):
            print(f"volume_{type}_{limit}.png uploaded to S3")
        else:
            print(f"volume_{type}_{limit}.png upload to S3 failed")


    else:
        print("Invalid type")    

sleep(40)

generate_gain_lose_image("increase", 100)
generate_gain_lose_image("decrease", 100)
generate_gain_lose_image("increase", 500)
generate_gain_lose_image("decrease", 500)
