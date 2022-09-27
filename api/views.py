from ctypes import c_void_p
from django.shortcuts import render
from content.models import Tag, News, NewsSources, NewsCategory, Project, Prices, Category, PublishedLog
from django.http import JsonResponse
from json_views.views import JSONDataView, JSONListView, PaginatedJSONListView
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

class TagsJSONList(JSONListView):
    model = Tag

class NewsJSONList(PaginatedJSONListView):
    model = News

    paginate_by = 10
    count_query = 'count'
    count_only  = False

    def get_queryset(self):
        if 'project' in self.kwargs:
            projects = list(self.kwargs['project'].split(',')).lower()
            print(projects)
            return News.objects.filter(projects__symbol__in=projects, status='PUBLISHED').order_by('-published_at')
        else:
            return News.objects.filter(status='PUBLISHED').order_by('-published_at')

class TopNewsJSONList(PaginatedJSONListView):
    model = News

    paginate_by = 10
    count_query = 'count'
    count_only  = False

    def get_queryset(self):
        
        platforms = ['twitter', 'telegram', 'instagram', 'facebook']
        
        if 'platform' in self.kwargs:
            platform = self.kwargs['platform'].lower()
        else:
            platform = ''

        if 'published' in self.kwargs:
            published = self.kwargs['published'].lower()
        else:
            published = ''

        if published == 'true' and platform in platforms:
            published_log = PublishedLog.objects.filter(platform=platform).values_list('news', flat=True)
            newsitems = News.objects.exclude(status='IGNORE').order_by('-published_at')
        elif published=='false' and platform in platforms:
            newsitems = News.objects.exclude(status='IGNORE').order_by('-published_at')
        else:
            newsitems = News.objects.exclude(status='IGNORE').order_by('-published_at')

        return_items = []
        for news in newsitems:
            if news.votes['important'] > 4:
                return_items.append(news)

        return return_items

class ProjectJSONList(PaginatedJSONListView):
    paginate_by = 50
    count_query = 'count'
    count_only  = False

    def get_queryset(self):
        return Project.objects.all().exclude(marketcap_rank__isnull=True).order_by('marketcap_rank')

class ProjectCategoriesJSONList(PaginatedJSONListView):
    paginate_by = 100
    count_query = 'count'
    count_only  = False

    def get_queryset(self):
        return Category.objects.all() 

class TagsAddView(LoginRequiredMixin,CreateView):
    model = Tag
    fields = ['name']

class PricesView(PaginatedJSONListView):
    paginate_by = 100
    count_query = 'count'
    count_only  = False

    def get_queryset(self):
        
        if 'coingecko_id' in self.request.GET:
            if Prices.objects.filter(project__coingecko_id=self.request.GET['coingecko_id']):
                return Prices.objects.filter(project__coingecko_id=self.request.GET['coingecko_id'])
            else:
                return {'error': 'Invalid coingecko_id'}
        else:
            return Prices.objects.filter(project__marketcap_rank__lte=1000).order_by('project__marketcap_rank')


class TopMoversUp(JSONListView):
    models = Prices

    def get_queryset(self):
        try:
            if self.kwargs['timeframe'] == '1h':
                if 'limit' in self.kwargs:
                    if self.kwargs['limit'] == '100':
                        return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_1h__isnull=True).order_by('-price_change_percent_1h')[0:9]
                    elif self.kwargs['limit'] == '500':
                        return Prices.objects.filter(project__marketcap_rank__lte=500).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_1h__isnull=True).order_by('-price_change_percent_1h')[0:9]
                    else:
                        return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_1h__isnull=True).order_by('-price_change_percent_1h')[0:9]
                else:                        
                    return Prices.objects.filter(project__marketcap_rank__lte=750).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_1h__isnull=True).order_by('-price_change_percent_1h')[0:9]
            
            elif self.kwargs['timeframe'] == '24h':
                if 'limit' in self.kwargs:
                    if self.kwargs['limit'] == '100':
                        return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_24h__isnull=True).order_by('-price_change_percent_24h')[0:9]
                    elif self.kwargs['limit'] == '500':
                        return Prices.objects.filter(project__marketcap_rank__lte=500).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_24h__isnull=True).order_by('-price_change_percent_24h')[0:9]
                    else:
                        return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_24h__isnull=True).order_by('-price_change_percent_24h')[0:9]
                else:                        
                    return Prices.objects.filter(project__marketcap_rank__lte=750).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_24h__isnull=True).order_by('-price_change_percent_24h')[0:9]                
            
            elif self.kwargs['timeframe'] == '7d':
                if 'limit' in self.kwargs:
                    if self.kwargs['limit'] == '100':
                        return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_7d__isnull=True).order_by('-price_change_percent_7d')[0:9]
                    elif self.kwargs['limit'] == '500':
                        return Prices.objects.filter(project__marketcap_rank__lte=500).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_7d__isnull=True).order_by('-price_change_percent_7d')[0:9]
                    else:
                        return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_7d__isnull=True).order_by('-price_change_percent_7d')[0:9]
                else:                        
                    return Prices.objects.filter(project__marketcap_rank__lte=750).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_7d__isnull=True).order_by('-price_change_percent_7d')[0:9]                
            
            else:    
                return Prices.objects.filter(project__marketcap_rank__lte=500).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_24h__isnull=True).order_by('-price_change_percent_24h')[0:9]
        except Exception as e:
            return {'error': f'Problems getting data with error: {e}'}


class TopMoversDown(JSONListView):
    models = Prices
    
    def get_queryset(self):
        try:
            if self.kwargs['timeframe'] == '1h':
                if 'limit' in self.kwargs:
                    if self.kwargs['limit'] == '100':
                        return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_1h__isnull=True).order_by('price_change_percent_1h')[0:9]
                    elif self.kwargs['limit'] == '500':
                        return Prices.objects.filter(project__marketcap_rank__lte=500).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_1h__isnull=True).order_by('price_change_percent_1h')[0:9]
                    else:
                        return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_1h__isnull=True).order_by('price_change_percent_1h')[0:9]
                else:                        
                    return Prices.objects.filter(project__marketcap_rank__lte=750).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_1h__isnull=True).order_by('price_change_percent_1h')[0:9]
            
            elif self.kwargs['timeframe'] == '24h':
                if 'limit' in self.kwargs:
                    if self.kwargs['limit'] == '100':
                        return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_24h__isnull=True).order_by('price_change_percent_24h')[0:9]
                    elif self.kwargs['limit'] == '500':
                        return Prices.objects.filter(project__marketcap_rank__lte=500).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_24h__isnull=True).order_by('price_change_percent_24h')[0:9]
                    else:
                        return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_24h__isnull=True).order_by('price_change_percent_24h')[0:9]
                else:                        
                    return Prices.objects.filter(project__marketcap_rank__lte=750).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_24h__isnull=True).order_by('price_change_percent_24h')[0:9]                
            
            elif self.kwargs['timeframe'] == '7d':
                if 'limit' in self.kwargs:
                    if self.kwargs['limit'] == '100':
                        return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_7d__isnull=True).order_by('price_change_percent_7d')[0:9]
                    elif self.kwargs['limit'] == '500':
                        return Prices.objects.filter(project__marketcap_rank__lte=500).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_7d__isnull=True).order_by('price_change_percent_7d')[0:9]
                    else:
                        return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_7d__isnull=True).order_by('price_change_percent_7d')[0:9]
                else:                        
                    return Prices.objects.filter(project__marketcap_rank__lte=750).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_7d__isnull=True).order_by('price_change_percent_7d')[0:9]                
            
            else:    
                return Prices.objects.filter(project__marketcap_rank__lte=500).exclude(project__marketcap_rank__isnull=True).exclude(price_change_percent_24h__isnull=True).order_by('price_change_percent_24h')[0:9]
        except Exception as e:
            return {'error': f'Problems getting data with error: {e}'}




class VolumeUp(JSONListView):
    models = Prices
    
    def get_queryset(self):
        if 'limit' in self.kwargs:
            if self.kwargs['limit'] == '100':
                return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(volume_change_percent_24h__isnull=True).order_by('-volume_change_percent_24h')[0:9]
            elif self.kwargs['limit'] == '500':
                return Prices.objects.filter(project__marketcap_rank__lte=500).exclude(project__marketcap_rank__isnull=True).exclude(volume_change_percent_24h__isnull=True).order_by('-volume_change_percent_24h')[0:9]
            else:
                return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(volume_change_percent_24h__isnull=True).order_by('-volume_change_percent_24h')[0:9]
        else:
            return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(volume_change_percent_24h__isnull=True).order_by('-volume_change_percent_24h')[0:9]

class VolumeDown(JSONListView):
    models = Prices                

    def get_queryset(self):
        if 'limit' in self.kwargs:
            if self.kwargs['limit'] == '100':
                return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(volume_change_percent_24h__isnull=True).order_by('volume_change_percent_24h')[0:9]
            elif self.kwargs['limit'] == '500':
                return Prices.objects.filter(project__marketcap_rank__lte=500).exclude(project__marketcap_rank__isnull=True).exclude(volume_change_percent_24h__isnull=True).order_by('volume_change_percent_24h')[0:9]
            else:
                return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(volume_change_percent_24h__isnull=True).order_by('volume_change_percent_24h')[0:9]
        else:
            return Prices.objects.filter(project__marketcap_rank__lte=100).exclude(project__marketcap_rank__isnull=True).exclude(volume_change_percent_24h__isnull=True).order_by('volume_change_percent_24h')[0:9]
