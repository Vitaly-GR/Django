from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('board.urls')),

]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
