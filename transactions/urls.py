from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views


urlpatterns = [
    path('payment/', views.payment, name='payment'),
    path('outcoming/', views.outcoming, name='outcoming'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)