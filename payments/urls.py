from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('payment/', views.payment_form, name='payment_form'),
    path('process_payment/', views.process_payment, name='process_payment'),
]
