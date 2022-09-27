from django.contrib import admin
from content.models import Project, Prices, News, NewsSources, Category, Tag, NewsCategory

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','name','sort_order','symbol','description','image_url','marketcap_rank')
    filter_display = ('name','symbol')
admin.site.register(Project, ProjectAdmin)

class PricesAdmin(admin.ModelAdmin):
    list_display = ('project', 'price', 'price_change_percent_24h','last_update','marketcap')
    filter_fields = ('project','price','price_change_percent_24h','last_update','volume_24h','volumen_change_percent_24h','marketcap')

admin.site.register(Prices, PricesAdmin)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id','title','type','article_url','image','source') 
    filter_fields = ('id','title','type','tags','source')

admin.site.register(News, NewsAdmin)

class NewsSourcesAdmin(admin.ModelAdmin):
    list_display = ('title','domain','region','path')
    filter_fields = ('domain','region','path')

admin.site.register(NewsSources, NewsSourcesAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_fields = ('name',)

admin.site.register(Tag, TagAdmin)

class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_fields = ('name',)

admin.site.register(NewsCategory, NewsCategoryAdmin)