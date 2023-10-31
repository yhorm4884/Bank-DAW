from django.urls import include, path

from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('deactivate/', views.deactivate_account, name='deactivate'),
    path('reactivate/<str:token>/', views.reactivate_account, name='reactivate'),
    path('', include('django.contrib.auth.urls')),
]
