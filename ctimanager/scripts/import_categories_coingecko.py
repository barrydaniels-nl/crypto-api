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

try:
    response = requests.get("https://api.coingecko.com/api/v3/coins/categories/list")

    for category in response.json():
        
        if Category.objects.filter(category_id=category['category_id']).exists():
            category = Category.objects.get(category_id=category['category_id'])
            category.name = category['name']
            category.save()
            print(f"Updating category {category['name']}")
        else:
            Category.objects.create(category_id=category['category_id'],name=category['name'])
            print(f"Creating category {category['name']}")

except Exception as e:
    print(e)

