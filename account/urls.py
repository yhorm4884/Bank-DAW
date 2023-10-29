# from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

urlpatterns = [
    # En esta primera url ya django tiene establecido las principales direcciones como un/login ...
    path('', include('django.contrib.auth.urls')),
    # Muestra el dashboard de la página
    path('', views.dashboard, name='dashboard'),
    # Redirije al metodo post de registrarse dentro de las vistas
    path('register/', views.register, name='register'),
    # Urls para la edición del perfil del usuario
    path('edit/', views.edit, name='edit'),
    path('deactivate/', views.deactivate_account, name='deactivate'),
    path('reactivate/<str:token>/', views.reactivate_account, name='reactivate'),
]
