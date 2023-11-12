from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('list_cards/', views.credit_card_list, name='credit_card_list'),
    path('my_cards/', views.credit_cards, name='credit_cards'),
    path('add/', views.add_credit_card, name='add_credit_card'),
    path('add-wa/<str:account_id>/', views.add_credit_card_without_account, name='add_credit_card_without_account'),
    path('block/<str:card_code>/', views.block_credit_card, name='block_credit_card'),
    path('delete/<str:card_code>/', views.delete_credit_card, name='delete_credit_card'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)