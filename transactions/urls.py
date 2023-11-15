from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'transactions'
urlpatterns = [
    path('payment/', views.payment, name='payment'),
    path('transfer/incoming/', views.incoming, name='incoming'),
    path('outcoming/', views.outcoming, name='outcoming'),
    path('transactions/<str:account>/', views.transactions_list, name='transactions_list'),
    path('transactions/', views.transactions, name='transactions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
