from django.urls import path
from content.views import NewsListView, NewsMonitorUpdateView, NewsMonitorView, NewsIgnoreView, ProjectsListView, ProjectsUpdateView, ProjectsDeleteView, PriceView, NewsListBlockView, NewsListBigBlockView, NewsMonitorApproveAll, StatusImagesView

app_name = 'content'

urlpatterns = [
    path('news-list/', NewsListView.as_view(), name='news-list'),
    path('news/', NewsListBlockView.as_view(), name='news-list-block'),
    path('newsblocks/', NewsListBigBlockView.as_view(), name='news-list-bigblock'),
    path('news-monitor', NewsMonitorView, name='news-monitor'),
    path('news-monitor-update/<int:pk>', NewsMonitorUpdateView.as_view(), name='news-monitor-update'),
    path('news-monitor-update-all', NewsMonitorApproveAll.as_view(), name='news-monitor-update-all'),
    path('news-delete/<int:newsid>', NewsIgnoreView, name='news-monitor-delete'),
    path('projects', ProjectsListView.as_view(), name='projects-list'),
    path('projects/<int:pk>/update', ProjectsUpdateView.as_view(), name='projects-update'),
    path('projects/<int:pk>/delete', ProjectsDeleteView.as_view(), name='projects-delete'),
    path('price', PriceView.as_view(), name='price-view'),
    path('status_images', StatusImagesView.as_view(), name='status-images'),
    ]