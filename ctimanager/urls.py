
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from content.views import NewsListView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('content/', include('content.urls')),
    path('api/', include('api.urls')),
    path('', NewsListView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
