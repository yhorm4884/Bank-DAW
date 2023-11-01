from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('list_cards/', views.credit_card_list, name='credit_card_list'),
    path('my_cards/', views.credit_cards, name='credit_cards'),
    path('add/', views.add_credit_card, name='add_credit_card'),
    path('block/<str:card_code>/', views.block_credit_card, name='block_credit_card'),
    path('delete/<str:card_code>/', views.delete_credit_card, name='delete_credit_card'),

]