from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views


urlpatterns = [
    path('payment/', views.payment, name='payment'),
    path('paymentform/', views.payment_form, name='paymentform'),
    path('incoming/', views.incoming, name='incoming'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)