from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.client_login, name='login'),
    path('register/', views.register, name='client_register'),
    path('',views.dashboard, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('deactivate/', views.deactivate_account, name='deactivate'),
    path('reactivate/<str:token>/', views.reactivate_account, name='reactivate'),
]
