############################################################################
## Django ORM Standalone Python Template
############################################################################
""" Here we'll import the parts of Django we need. It's recommended to leave
these settings as is, and skip to START OF APPLICATION section below """

# Turn off bytecode generation
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

"""
Project
    coingecko_id = models.IntegerField(blank=False)
    name = models.CharField(max_length=100,blank=False)
    description = models.TextField(blank=True,null=True)
    symbol = models.CharField(max_length=10, blank=False)
    image_url = models.CharField(max_length=100)
    proof_type = models.CharField(max_length=100, blank=False)
    algorithm = models.CharField(max_length=100)
    sort_order = models.IntegerField(blank=False)
    last_update = models.DateTimeField(auto_now=True)
"""

for page_number in range(1,5):

    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page={page_number}&sparkline=false&price_change_percentage=1h%2C24h%2C7d"

    response = requests.get(url)

    for coin in response.json():

        try:
            coingecko_id = coin['id']
            name = coin['name'][0:99]
            symbol = coin['symbol'][0:10]
            image_url = coin['image']
            current_price = coin['current_price']
            price_change_24h = coin['price_change_24h']
            marketcap_rank = coin['market_cap_rank']
            marketcap_change_percent_24h = coin['market_cap_change_percentage_24h']
            sort_order = coin['market_cap_rank']
            circulating_supply = coin['circulating_supply']
            total_supply = coin['total_supply']
            max_supply = coin['max_supply']
            ath = coin['ath']
            ath_change_percentage = coin['ath_change_percentage']
            ath_date = coin['ath_date']
            atl = coin['atl']
            atl_change_percentage = coin['atl_change_percentage']
            atl_date = coin['atl_date']
            last_updated = coin['last_updated']
            price_change_percentage_1h = coin['price_change_percentage_1h_in_currency']
            price_change_percentage_24h = coin['price_change_percentage_24h_in_currency']
            price_change_percentage_7d = coin['price_change_percentage_7d_in_currency']

            if Project.objects.filter(coingecko_id=coingecko_id).exists():
                project = Project.objects.get(coingecko_id=coingecko_id)
                project.name = name
                project.symbol = symbol
                #project.image_url = image_url
                project.sort_order = sort_order
                project.marketcap_rank = marketcap_rank
                project.ath = ath
                project.ath_change_percentage = ath_change_percentage
                project.ath_date = ath_date
                project.atl = atl
                project.atl_change_percentage = atl_change_percentage
                project.atl_date = atl_date
                project.last_updated = last_updated
                project.circulating_supply = circulating_supply
                project.total_supply = total_supply
                project.max_supply = max_supply
                project.save()
                
                price = Prices.objects.get(project=project)
                price.price = current_price
                price.price_change_24h=price_change_24h
                price.price_change_percent_1h=price_change_percentage_1h
                price.price_change_percent_24h=price_change_percentage_24h
                price.price_change_percent_7d=price_change_percentage_7d
                price.marketcap_rank=marketcap_rank
                price.marketcap = coin['market_cap']
                price.marketcap_change_24h = coin['market_cap_change_24h']
                price.marketcap_change_percent_24h = coin['market_cap_change_percentage_24h']
                price.high_24h = coin['high_24h']
                price.low_24h = coin['low_24h']
                price.last_updated = coin['last_updated']
                price.save()
                print(f"Updating entry for {project.name}")

            else:
                project_id = Project.objects.create(coingecko_id=coingecko_id, name=name, symbol=symbol)
                project = Project.objects.get(pk=project_id.pk)
                project.image_url = image_url
                project.sort_order = sort_order
                project.marketcap_rank = marketcap_rank
                project.ath = ath
                project.ath_change_percentage = ath_change_percentage
                project.ath_date = ath_date
                project.atl = atl
                project.atl_change_percentage = atl_change_percentage
                project.atl_date = atl_date
                project.last_updated = last_updated
                project.circulating_supply = circulating_supply
                project.total_supply = total_supply
                project.max_supply = max_supply
                project.save()

                Prices.objects.create(project=project, price=current_price)
                price = Prices.objects.get(project=project)
                price.price = current_price
                price.price_change_24h=price_change_24h
                price.price_change_percent_1h=price_change_percentage_1h
                price.price_change_percent_24h=price_change_percentage_24h
                price.price_change_percent_7d=price_change_percentage_7d
                price.market_cap_rank=marketcap_rank
                price.marketcap = coin['market_cap']
                price.marketcap_change_24h = coin['market_cap_change_24h']
                price.marketcap_change_percent_24h = coin['market_cap_change_percentage_24h']
                price.high_24h = coin['high_24h']
                price.low_24h = coin['low_24h']
                price.last_updated = coin['last_updated']
                price.save()

                print(f"Creating entry for {project.name}")

        except Exception as e:
            print(f"Error adding project with error {e}")
            print(f"{coingecko_id} {name} {symbol}")
            

