from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('accounts/', views.accounts, name='accounts'),
    path('edit_alias/<int:account_id>/', views.edit_alias, name='edit_alias'),
    path('deactivate/<int:account_id>/', views.deactivate_account, name='deactivate'),
    path('reactivate/<str:token>/', views.reactivate_account, name='reactivate'),
    path('edit_alias/<int:account_id>/', views.edit_alias, name='edit_alias'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
