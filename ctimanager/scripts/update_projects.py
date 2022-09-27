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
import re

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

projects = Project.objects.order_by('marketcap_rank').exclude(marketcap_rank__isnull=True).exclude(coinmarketcap_id__isnull=True)

for project in projects:
    print(project.symbol)
    project.symbol = project.symbol.lower()
    project.description = striphtml(project.description)
    project.save()