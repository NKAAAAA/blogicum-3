from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Основные маршруты приложения blog
    path('auth/', include('django.contrib.auth.urls')),  # Встроенные маршруты аутентификации
    path('pages/', include('pages.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)