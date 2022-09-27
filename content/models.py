from django.db import models
from datetime import datetime

from django.db.models.fields.json import JSONField

class Category(models.Model):
    category_id = models.CharField(max_length=500)
    name = models.CharField(max_length=500,blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Tag(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tags"

class Project(models.Model):
    coingecko_id = models.CharField(max_length=255,blank=False,null=True)
    coinmarketcap_id = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=500,blank=False)
    description = models.TextField(blank=True,null=True)
    homepage = models.URLField(blank=True, null=True)
    symbol = models.CharField(max_length=100, blank=False)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    proof_type = models.CharField(max_length=100, blank=True, null=True)
    algorithm = models.CharField(max_length=100, blank=True, null=True)
    sort_order = models.IntegerField(blank=True, null=True)
    marketcap_rank = models.IntegerField(blank=True, null=True)
    coingecko_rank = models.IntegerField(blank=True, null=True)
    circulating_supply = models.FloatField(blank=True, null=True)
    total_supply = models.FloatField(blank=True, null=True)
    max_supply = models.FloatField(blank=True, null=True)
    ath = models.FloatField(blank=True, null=True)
    ath_change_percentage = models.FloatField(blank=True, null=True)
    ath_date = models.DateTimeField(blank=True, null=True)
    atl = models.FloatField(blank=True, null=True)
    atl_change_percentage = models.FloatField(blank=True, null=True)
    atl_date = models.DateTimeField(blank=True, null=True)
    categories = models.ManyToManyField(Category)
    genesis_date = models.DateTimeField(blank=True, null=True)
    developer_score = models.FloatField(blank=True, null=True)
    community_score = models.FloatField(blank=True, null=True)
    liquidity_score = models.FloatField(blank=True, null=True)
    sentiment_positive_percentage = models.FloatField(blank=True, null=True)
    sentiment_negative_percentage = models.FloatField(blank=True, null=True)
    STATUS_OPTIONS = (
        ('ACTIVE','Active'),
        ('BLOCKED', 'Blocked')
    )
    status = models.CharField(max_length=50,choices=STATUS_OPTIONS,default='ACTIVE')   
    last_update = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            'name': self.name,
            'symbol': self.symbol,
            'image':self.image_url,
            'description':self.description,
            'homepage':self.homepage,
            'sort_order':self.marketcap_rank,
            'total_supply':self.total_supply,
            'circulating_supply':self.circulating_supply,
            'max_supply':self.max_supply,
            'sentiment_positive_percentage':self.sentiment_positive_percentage,
            'sentiment_negative_percentage':self.sentiment_negative_percentage,
            'status':self.status,
            'developer_score':self.developer_score,
            'community_score':self.community_score,
            'liquidity_score':self.liquidity_score,
            'categories':[category.name for category in self.categories.all()],
            'ath':self.ath,
            'ath_change_percentage':self.ath_change_percentage,
            'ath_date':self.ath_date,
            'atl':self.atl,
            'atl_change_percentage':self.atl_change_percentage,
            'atl_date':self.atl_date,
            'coinmarketcap_id': self.coinmarketcap_id,
            'last_update':self.last_update,

        }  

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-pk']
        verbose_name_plural = "Projects"

class Prices(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    price = models.FloatField(blank=False)
    price_change_24h = models.FloatField(blank=True, null=True)
    price_change_percent_1h = models.FloatField(blank=True, null=True)
    price_change_percent_24h = models.FloatField(blank=True, null=True)
    price_change_percent_7d = models.FloatField(blank=True, null=True)
    volume_1h = models.FloatField(blank=True, null=True)
    volume_24h = models.FloatField(blank=True, null=True)
    volume_change_percent_24h = models.FloatField(blank=True, null=True)
    volume_7d = models.FloatField(blank=True, null=True)
    marketcap_rank = models.IntegerField(blank=True, null=True)
    marketcap = models.FloatField(blank=True, null=True)
    marketcap_change_24h = models.FloatField(blank=True, null=True)
    marketcap_change_percent_24h = models.FloatField(blank=True, null=True)
    high_24h = models.FloatField(blank=True, null=True)
    low_24h = models.FloatField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project.name

    def serialize(self):
        return {
            'name': self.project.name,
            'symbol': self.project.symbol,
            'image':self.project.image_url,
            'price_usd': self.price,
            'price_change_percent_1h': self.price_change_percent_1h,
            'price_change_percent_24h': self.price_change_percent_24h,
            'price_change_percent_7d': self.price_change_percent_7d,    
            'volume_1h': self.volume_1h,
            'volume_24h': self.volume_24h,
            'volume_change_percent_24h': self.volume_change_percent_24h,
            'volume_7d': self.volume_7d,
            'marketcap': self.marketcap,
            'high_24h': self.high_24h,
            'low_24h': self.low_24h,
            'last_update': self.last_update,
            'sort_order': self.project.marketcap_rank,
        }        

    class Meta:
        verbose_name_plural = "Prices"

class NewsSources(models.Model):
    title = models.TextField(blank=False, null=True)
    domain = models.CharField(max_length=255, blank=False, null=True)
    rss_url = models.URLField(blank=True, null=True)
    article_selector = models.CharField(max_length=1024, blank=True, null=True)
    article_selector_id = models.CharField(max_length=1024, blank=True, null=True)
    region = models.CharField(max_length=5, blank=True, null=True)
    path = models.CharField(max_length=100, blank=True, null=True)
    manual_import = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "NewsSources"

class NewsCategory(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "NewsCategories"


class News(models.Model):
    cryptopanic_id = models.IntegerField(blank=True, null=True)
    cryptopanic_url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=500, blank=False, null=True)
    excerpt = models.TextField(blank=True, null=True)
    full_article = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, blank=False)
    domain = models.CharField(max_length=100, blank=True, null=True)
    projects = models.ManyToManyField(Project, blank=True)
    categories = models.ManyToManyField(NewsCategory, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    # Note! The JSON1 module needs to be enables in SQL, if you get an error this might be the problem. 
    votes = models.JSONField(blank=True, null=True)
    article_url = models.URLField(blank=False, null=True)
    image = models.URLField(blank=True, null=True)
    source = models.ForeignKey(NewsSources, on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    SENTIMENT_OPTIONS = (
        ('POSITIVE','Positive'),
        ('NEUTRAL','Neutral'),
        ('NEGATIVE','Negative'))
    sentiment = models.CharField(max_length=50,choices=SENTIMENT_OPTIONS,blank=True,null=True)
    STATUS_OPTIONS = (
        ('RECEIVED','Received'),
        ('PUBLISHED','Placed in feed'),
        ('IGNORE', 'Ignore post')
    )
    status = models.CharField(max_length=50,choices=STATUS_OPTIONS,default='RECEIVED')    
    EXPERT_LEVELS = (('BASIC','Basic'),
                     ('INTERMEDIATE','Intermediate'),
                     ('PRO','Pro'))
    expert_level = models.CharField(max_length=50,choices=EXPERT_LEVELS,default=EXPERT_LEVELS[2][0],blank=False,null=True)

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            'title': self.title,
            'excerpt': self.excerpt,
            'full_article': self.full_article,
            'type': self.type,
            'domain': self.domain,
            'projects': [p.name for p in self.projects.all()],
            'categories': [c.name for c in self.categories.all()],
            'tags': [t.name for t in self.tags.all()],
            'votes': self.votes,
            'article_url': self.article_url,
            'image': self.image,
            'source': self.source.domain,
            'published_at': self.published_at,
            'sentiment': self.sentiment,
            'status': self.status,
            'expert_level': self.expert_level,
            'id': self.id
        }

    class Meta:
        ordering = ["published_at"]
        verbose_name_plural = "News"


class PublishedLog(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, blank=False, null=False)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.news.title

    class Meta:
        verbose_name_plural = "PublishedLog"

