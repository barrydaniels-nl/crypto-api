from PIL import Image, ImageFont, ImageDraw
import requests
from io import BytesIO
from datetime import datetime, timezone
import pytz
import os
import sys
from time import sleep
import boto3

project_path = "../"
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

def get_stats(type, timeframe, limit):

    if type == "gainers":
        url = f"{HOSTNAME}/api/prices/gainers/{timeframe}/{limit}"
    elif type == "losers":
        url = f"{HOSTNAME}/api/prices/losers/{timeframe}/{limit}"
    
    response = requests.get(url)
    data = response.json()
    return data   

def calculate_spaces(price):
    spaces_string = ""
    price = str(round(price,2))
    price = price.replace(".", "").replace("-", "")
    price_len = len(price)
    spaces = 5 - price_len
    for space in range(spaces):
        spaces_string = " " + spaces_string
    return spaces_string

def generate_gain_lose_image(timeframe):

    if timeframe == "24h" or timeframe == "7d":

        data_gainers = get_stats("gainers", timeframe, 500)
        data_losers = get_stats("losers", timeframe, 500)

        if timeframe == "24h":
            image_name = f"instagram/templates/insta_gainers_losers_24h.png"
        elif timeframe == "7d":
            image_name = f"instagram/templates/insta_gainers_losers_7d.png"

        template_image = Image.open(image_name)
        
        project_font = ImageFont.truetype("instagram/fonts/Aileron-Regular.otf", 48)
        symbol_font = ImageFont.truetype("instagram/fonts/Aileron-Light.otf", 20)
        percentage_font = ImageFont.truetype("instagram/fonts/Aileron-Regular.otf", 48)
        footer_font = ImageFont.truetype("instagram/fonts/Aileron-Bold.otf", 24)
        date_font = ImageFont.truetype("instagram/fonts/Aileron-Regular.otf", 24)
        
        publish_date = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")

        # Draw gainers
        for i in range(0,5):
            name = data_gainers['prices_list'][i]["name"]
            symbol = data_gainers['prices_list'][i]["symbol"]

            spaces = calculate_spaces(data_gainers['prices_list'][i][f"price_change_percent_{timeframe}"])
            if data_gainers['prices_list'][i][f"price_change_percent_{timeframe}"] > 0:
                percentage = "+" + str(data_gainers['prices_list'][i][f"price_change_percent_{timeframe}"]) + "%"
            else:
                percentage = "-" + str(data_gainers['prices_list'][i][f"price_change_percent_{timeframe}"]) + "%"
            percentage = spaces + str(round(data_gainers['prices_list'][i][f"price_change_percent_{timeframe}"],2)) + " %"
            img_response = requests.get(data_gainers['prices_list'][i]["image"])
            logo_image = Image.open(BytesIO(img_response.content)).resize((80, 80))
            template_image.convert('RGBA')
            template_image.paste(logo_image, (130, (320 + (i * 136))), logo_image.convert('RGBA'))                            
            # add text
            draw = ImageDraw.Draw(template_image)
            if i==0: 
                draw.text((248, 326), name, font=project_font, fill=(210, 210, 210))
                if float(data_gainers['prices_list'][i][f"price_change_percent_{timeframe}"])>0:
                    draw.text((807, 326), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((807, 326), str(percentage), font=percentage_font, fill=(246, 88, 88))
            
            if i==1:
                draw.text((248, 467), name, font=project_font, fill=(210, 210, 210))
                if float(data_gainers['prices_list'][i][f"price_change_percent_{timeframe}"])>0:
                    draw.text((807, 467), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((807, 467), str(percentage), font=percentage_font, fill=(246, 88, 88))

            if i==2:
                draw.text((248, 600), name, font=project_font, fill=(210, 210, 210))
                if float(data_gainers['prices_list'][i][f"price_change_percent_{timeframe}"])>0:
                    draw.text((807, 600), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((807, 600), str(percentage), font=percentage_font, fill=(246, 88, 88))

            if i==3:
                draw.text((248, 738), name, font=project_font, fill=(210, 210, 210))
                if float(data_gainers['prices_list'][i][f"price_change_percent_{timeframe}"])>0:
                    draw.text((807, 738), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((807, 738), str(percentage), font=percentage_font, fill=(246, 88, 88))
            if i==4:
                draw.text((248, 870), name, font=project_font, fill=(210, 210, 210))
                if float(data_gainers['prices_list'][i][f"price_change_percent_{timeframe}"])>0:
                    draw.text((807, 870), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((807, 870), str(percentage), font=percentage_font, fill=(246, 88, 88))
        
        # Draw losers
        for i in range(0,5):
            name = data_losers['prices_list'][i]["name"]
            symbol = data_gainers['prices_list'][i]["symbol"]

            spaces = calculate_spaces(data_losers['prices_list'][i][f"price_change_percent_{timeframe}"])
            if data_losers['prices_list'][i][f"price_change_percent_{timeframe}"] > 0:
                percentage = "+" + str(data_losers['prices_list'][i][f"price_change_percent_{timeframe}"]) + "%"
            else:
                percentage = "-" + str(data_losers['prices_list'][i][f"price_change_percent_{timeframe}"]) + "%"
            percentage = spaces + str(round(data_losers['prices_list'][i][f"price_change_percent_{timeframe}"],2)) + " %"
            img_response = requests.get(data_losers['prices_list'][i]["image"])
            logo_image = Image.open(BytesIO(img_response.content)).resize((80, 80))
            template_image.convert('RGBA')
            template_image.paste(logo_image, (130, (1219 + (i * 136))), logo_image.convert('RGBA'))                            
            # add text
            draw = ImageDraw.Draw(template_image)
            if i==0: 
                draw.text((248, 1225), name, font=project_font, fill=(210, 210, 210))
                if float(data_losers['prices_list'][i][f"price_change_percent_{timeframe}"])>0:
                    draw.text((807, 1225), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((807, 1225), str(percentage), font=percentage_font, fill=(246, 88, 88))
            
            if i==1:
                draw.text((248, 1360), name, font=project_font, fill=(210, 210, 210))
                if float(data_losers['prices_list'][i][f"price_change_percent_{timeframe}"])>0:
                    draw.text((807, 1360), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((807, 1360), str(percentage), font=percentage_font, fill=(246, 88, 88))

            if i==2:
                draw.text((248, 1495), name, font=project_font, fill=(210, 210, 210))
                if float(data_losers['prices_list'][i][f"price_change_percent_{timeframe}"])>0:
                    draw.text((807, 1495), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((807, 1495), str(percentage), font=percentage_font, fill=(246, 88, 88))

            if i==3:
                draw.text((248, 1635), name, font=project_font, fill=(210, 210, 210))
                if float(data_losers['prices_list'][i][f"price_change_percent_{timeframe}"])>0:
                    draw.text((807, 1635), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((807, 1635), str(percentage), font=percentage_font, fill=(246, 88, 88))
            if i==4:
                draw.text((248, 1770), name, font=project_font, fill=(210, 210, 210))
                if float(data_losers['prices_list'][i][f"price_change_percent_{timeframe}"])>0:
                    draw.text((807, 1770), str(percentage), font=percentage_font, fill=(101, 246, 88))
                else:
                    draw.text((807, 1770), str(percentage), font=percentage_font, fill=(246, 88, 88))

        """
        draw.text((22, 446), "@cryptonewscasters", font=footer_font, fill=(255, 255, 255))
        """

        draw.text((671, 1870), f"{publish_date} UTC", font=date_font, fill=(135, 168, 160))

        template_image.save(f"instagram/generated_images/insta_gainers_losers_{timeframe}.png")
        
        if upload_image_to_s3(f"instagram/generated_images/insta_gainers_losers_{timeframe}.png", f"insta_gainers_losers_{timeframe}.png"):
            print(f"Uploaded insta_gainers_losers_{timeframe}.png to S3")
        else:
            print(f"Failed to upload insta_gainers_losers_{timeframe}.png to S3")
  
    else:
        print("Invalid timeframe")
  



generate_gain_lose_image("24h")
generate_gain_lose_image("7d")