
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# определение маршрутов URL к приложениям
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main.urls', 'main'), namespace='main')),
    path('profile/', include(('user.urls', 'user'), namespace='user')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
