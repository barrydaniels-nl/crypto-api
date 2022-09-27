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

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))


projects = Project.objects.order_by('marketcap_rank').exclude(marketcap_rank__isnull=True).exclude(coinmarketcap_id__isnull=True)

ids = []
for project in projects:
    ids.append(str(project.coinmarketcap_id))

id_parts = chunks(ids, 250)


for id_part in id_parts:
    
    id_list = ','.join(id_part)

    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?convert=usd&id={id_list}"  
    
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.environ.get('COINMARKETCAP_APIKEY'),
    }

    response = requests.get(url, headers=headers)
    

    for symbol in response.json()['data']:
        
        volume_change_24h = response.json()['data'][symbol]['quote']['USD']['volume_change_24h']
        coinmarketcap_id = response.json()['data'][symbol]['id']
        try:
            price = Prices.objects.get(project__coinmarketcap_id=coinmarketcap_id)
            price.volume_change_percent_24h = volume_change_24h
            price.save()
            print(f"Updating volume change for project: {response.json()['data'][symbol]['name']}")
        except Exception as e:
            print(f"Problem updating volume change for project: {response.json()['data'][symbol]['name']}")