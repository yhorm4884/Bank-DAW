from django.urls import path

from . import views

urlpatterns = [
    path('',views.dashboard, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='client_register'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('deactivate/', views.deactivate_account, name='deactivate'),
    path('reactivate/<str:token>/', views.reactivate_account, name='reactivate'),
]
