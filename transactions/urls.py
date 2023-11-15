from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('payment/', views.payment, name='payment'),
    path('transfer/incoming/', views.incoming, name='incoming'),
    path('outcoming/', views.outcoming, name='outcoming'),
    path('transactions/', views.transactions, name='transactions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
