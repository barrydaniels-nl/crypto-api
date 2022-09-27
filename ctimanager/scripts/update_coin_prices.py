############################################################################
## Django ORM Standalone Python Template
############################################################################

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
from time import sleep

sleep(20)

"""
class Prices(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    price = models.FloatField(blank=False)
    price_change_24h = models.FloatField(blank=True, null=True)
    price_change_percent_1h = models.FloatField(blank=True, null=True)
    price_change_percent_24h = models.FloatField(blank=True, null=True)
    price_change_percent_7d = models.FloatField(blank=True, null=True)
    volume_24h = models.FloatField(blank=True, null=True)
    marketcap_rank = models.IntegerField(blank=True, null=True)
    marketcap = models.FloatField(blank=True, null=True)
    marketcap_change_24h = models.FloatField(blank=True, null=True)
    marketcap_change_percent_24h = models.FloatField(blank=True, null=True)
    high_24h = models.FloatField(blank=True, null=True)
    low_24h = models.FloatField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
"""

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))


projects = Project.objects.order_by('marketcap_rank').exclude(marketcap_rank__isnull=True)

symbols = []
for project in projects:
    symbols.append(project.coingecko_id)

symbol_parts = chunks(symbols, 500)

for symbol_part in symbol_parts:
    
    symbol_list = ','.join(symbol_part)

    prices_url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol_list}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=false"
    
    
    proxies=dict(http='socks5://84.107.32.223:1080', https='socks5://84.107.32.223:1080')

    price_response = requests.get(prices_url, proxies=proxies)

    if price_response.status_code != 200:
        print(price_response.status_code)
        print(price_response.text)

    for coin in price_response.json():

        try:

            project = Project.objects.get(coingecko_id=coin)
            
            if not Prices.objects.filter(project=project).exists():
                Prices.objects.create(project=project, price=price_response.json()[coin]['usd'], price_change_percent_24h = price_response.json()[coin]['usd_24h_change'], volume_24h = price_response.json()[coin]['usd_24h_vol'], marketcap = price_response.json()[coin]['usd_market_cap'])
                print(f"Created new project for {project.name}")
            else:    
                prices = Prices.objects.get(project=project)    
                prices.price = price_response.json()[coin]['usd']
                prices.price_change_percent_24h = price_response.json()[coin]['usd_24h_change']
                prices.volume_24h = price_response.json()[coin]['usd_24h_vol']
                prices.marketcap = price_response.json()[coin]['usd_market_cap']
                prices.save()
                print(f"Updating price for {project.name}")
        
        except Exception as e:
            print(f"Error updating price for {project.name} with error: {e}")




