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
from django.utils import timezone
django.setup()

# Import your models for use in your script
from content.models import *

############################################################################
## START OF APPLICATION
############################################################################
import requests
from datetime import datetime
import time

"""
Project
    coingecko_id = models.CharField(max_length=255,blank=False,null=True)
    name = models.CharField(max_length=100,blank=False)
    description = models.TextField(blank=True,null=True)
    homepage = models.URLField(blank=False, null=True)
    symbol = models.CharField(max_length=10, blank=False)
    image_url = models.CharField(max_length=100, blank=True, null=True)
    proof_type = models.CharField(max_length=100, blank=True, null=True)
    algorithm = models.CharField(max_length=100, blank=True, null=True)
    sort_order = models.IntegerField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    ath = models.FloatField(blank=True, null=True)
    ath_date = models.DateTimeField(blank=True, default=datetime.now)
    categories = models.ManyToManyField(Category)
"""


for project in Project.objects.all():

    url = f"https://api.coingecko.com/api/v3/coins/{project.coingecko_id}?tickers=true&market_data=true&community_data=true&developer_data=false&sparkline=false"
    
    try:
        response = requests.get(url=url, timeout=20)
    except Exception as e:
        print(f"Error getting URL {url} with error {e}")

    if response.status_code == 200:

        coingecko_id = project.coingecko_id
        try:
            name = response.json()['name'][0:98]
        except Exception as e:
            name = ""
        
        try:
            description = response.json()['description']['en']
        except Exception as e:
            description = ""

        try:
            homepage = list(response.json()['links']['homepage'])[0]

        except Exception as e:
            homepage = ""

        try:
            image_url = response.json()['image']['large']
        except Exception as e:
            image_url = ""

        try:
            coingecko_rank = response.json()['coingecko_rank']
        except Exception as e:
            coingecko_rank = None

        try:
            algorithm = response.json()['hashing_algorithm']
        except Exception as e:
            algorithm = ""

        try:
            ath = response.json()['market_data']['ath']['usd']
        except Exception as e:
            ath = 0
        
        try:
            ath_date = response.json()['market_data']['ath_date']['usd']
        except Exception as e:
            ath_date = timezone.now()
        
        try :
            developer_score = response.json()['developer_score']
        except Exception as e:
            developer_score = None

        try:
            community_score = response.json()['community_score']
        except Exception as e:
            community_score = None

        try:
            liquidity_score = response.json()['liquidity_score']
        except Exception as e:
            liquidity_score = None            

        try:
            sentiment_positive_percentage = response.json()['sentiment_votes_up_percentage']
        except Exception as e:
            sentiment_positive_percentage = None     

        try:
            sentiment_negative_percentage = response.json()['sentiment_votes_down_percentage']
        except Exception as e:
            sentiment_negative_percentage = None     


        try:
            if Project.objects.filter(coingecko_id=coingecko_id).exists():
                project = Project.objects.get(coingecko_id=coingecko_id)
                project.name = name
                project.description = description
                project.homepage = homepage
                project.image_url = image_url
                project.coingecko_rank = coingecko_rank
                project.ath = ath
                project.ath_date = ath_date
                project.developer_score = developer_score
                project.community_score = community_score
                project.liquidity_score = liquidity_score
                project.sentiment_positive_percentage = sentiment_positive_percentage
                project.sentiment_positive_percentage = sentiment_negative_percentage
                project.save()

                try:
                    for category in response.json()['categories']:
                        cat_obj = Category.objects.get(name=category)
                        project.categories.add(cat_obj)
                        project.save()
                except Exception as e:
                    print(f"Error adding categories with error {e} category: {category}")

                print(f"Updated project {name}")
            else:
                try:
                    project = Project.objects.create(coingecko_id=coingecko_id,
                                                    name=name,
                                                    description=description,
                                                    homepage=homepage,
                                                    image_url=image_url,
                                                    coingecko_rank=coingecko_rank,
                                                    ath=ath,
                                                    ath_date=ath_date,
                                                    developer_score=developer_score,
                                                    community_score=community_score,
                                                    liquidity_score=liquidity_score,
                                                    sentiment_positive_percentage=sentiment_positive_percentage,
                                                    sentiment_negative_percentage=sentiment_negative_percentage)

                    print(f"Adding project {response.json()['name']} ({response.json()['symbol']}) with sort_order {response.json()['sort_order']}")    
                except Exception as e:
                    print(f"Error adding project with error {e}")
                    continue
                
        except Exception as e:
            print(f"Error updating coin data with error: {e}")

    else:
        time.sleep(1)