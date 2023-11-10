from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'transfers'

urlpatterns = [
    path('incoming', views.incoming, name='incoming'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
