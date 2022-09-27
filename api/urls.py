from django.urls import path
from api.views import TagsJSONList, NewsJSONList, TopNewsJSONList, ProjectJSONList, TagsAddView, PricesView, ProjectCategoriesJSONList, TopMoversUp, TopMoversDown, VolumeUp, VolumeDown

app_name = 'api'

urlpatterns = [
    path('tags', TagsJSONList.as_view(), name='tags-list'),
    path('tags/add', TagsAddView.as_view(), name='tags-add'),
    path('news', NewsJSONList.as_view(), name='news-list'),
    path('topnews', TopNewsJSONList.as_view(), name='news-list'),
    path('projects', ProjectJSONList.as_view(), name='project-list'),
    path('projects/categories', ProjectCategoriesJSONList.as_view(), name='project-categories'),
    path('prices', PricesView.as_view(), name='prices-list'),
    path('prices/gainers', TopMoversUp.as_view(), name='prices-up'),
    path('prices/gainers/<str:timeframe>', TopMoversUp.as_view(), name='prices-up-timeframe'),
    path('prices/gainers/<str:timeframe>/<int:limit>', TopMoversUp.as_view(), name='prices-up-timeframe-limit'),
    path('prices/losers', TopMoversDown.as_view(), name='prices-up'),
    path('prices/losers/<str:timeframe>', TopMoversDown.as_view(), name='prices-up'),
    path('prices/losers/<str:timeframe>/<int:limit>', TopMoversDown.as_view(), name='prices-up-timeframe-limit'),
    path('prices/volume_decrease', VolumeDown.as_view(), name='volume-decrease'),
    path('prices/volume_decrease/<int:limit>', VolumeDown.as_view(), name='volume-decrease-limit'),
    path('prices/volume_increase', VolumeUp.as_view(), name='volume-increase'),
    path('prices/volume_increase/<int:limit>', VolumeUp.as_view(), name='volume-increase-limit')
    ]