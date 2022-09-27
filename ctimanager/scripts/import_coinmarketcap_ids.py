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

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?listing_status=active"

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.environ.get('COINMARKETCAP_APIKEY'),
}

response = requests.get(url, headers=headers).json()

for project in response['data']:
    try:
        cmc_symbol = project['symbol'].lower()
        p = Project.objects.get(symbol=cmc_symbol)
        p.coinmarketcap_id = project['id']
        p.save()
        print(project['id'], project['symbol'].lower())
        print("Updated: ", project['symbol'])
    except Exception as e:
        pass
        