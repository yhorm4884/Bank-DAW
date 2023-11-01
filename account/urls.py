from django.urls import include, path

from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('deactivate/', views.deactivate_account, name='deactivate'),
    path('reactivate/<str:token>/', views.reactivate_account, name='reactivate'),
]
