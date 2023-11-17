from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'transactions'
urlpatterns = [
    path('payment/', views.payment, name='payment'),
    path('transfer/incoming/', views.incoming, name='incoming'),
    path('transfer/outcoming/', views.outcoming, name='outcoming'),
    path('movements/', views.movements, name='movements'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
