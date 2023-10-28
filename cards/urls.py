from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('add/', views.add_credit_card, name='add_credit_card'),
    # path('delete/<int:id>/', views.delete_credit_card, name='delete_credit_card'),
    path('', views.credit_card_list, name='credit_card_list'),
]