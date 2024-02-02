from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'clients'
urlpatterns = [

    path('', views.dashboard, name='home'),
    path('register/', views.register, name='register'),
    path('accounts/', views.accounts, name='accounts'),
    path('account-details/<int:account_id>/', views.account_details, name='account-details'),
    path('add-money/<int:account_id>/', views.add_money, name='add-money'),
    path('edit-alias/<int:account_id>/', views.edit_alias, name='edit-alias'),
    path('deactivate/<int:account_id>/', views.deactivate_account, name='deactivate'),
    path('reactivate/<str:token>/', views.reactivate_account, name='reactivate'),
    path('edit-alias/<int:account_id>/', views.edit_alias, name='edit-alias'),
   
    
    # URLs relacionadas con tarjetas
    path('list_cards/', views.credit_card_list, name='credit_card_list'),
    path('my_cards/', views.credit_cards, name='credit_cards'),
    path('add/', views.add_credit_card, name='add_credit_card'),
    path('add-wa/<str:account_id>/', views.add_credit_card_without_account, name='add_credit_card_without_account'),
    path('block/<str:card_code>/', views.block_credit_card, name='block_credit_card'),
    path('unblock/<str:card_code>/', views.reactivate_credit_card, name='reactivate_credit_card'),
    path('delete/<str:card_code>/', views.delete_credit_card, name='delete_credit_card'),

    # URLs relacionadas con cuentas
    path('register-account/', views.client_register, name='client_register'),
    path('login/', views.client_login, name='login'),
    path('accounts/', views.accounts, name='accounts'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('account-details/<int:account_id>/', views.account_details, name='account_details'),
    path('add-money/<int:account_id>/', views.add_money, name='add_money'),
    path('edit-alias/<int:account_id>/', views.edit_alias, name='edit_alias'),
    path('deactivate-client/<int:client_id>/', views.deactivate_client, name='deactivate_client'),
    path('client/reactivate/<str:token>/', views.reactivate_client, name='reactivate'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
