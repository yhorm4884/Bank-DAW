"""
URL configuration for bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from clients import views as cliente
from django.conf.urls.i18n import i18n_patterns

#Listado donde se almacenan todas las urls.
urlpatterns = []

# Url que no se deben internacionalizar.
urlpatterns_base = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('__reload__/', include('django_browser_reload.urls')),
]

# Utilizando i18n_patterns para aplicar la internacionalización a las URL de clientes, transacciones y otras...
urlpatterns += i18n_patterns(
    path('', cliente.dashboard, name='home'),
    path('', include('clients.urls')),
    path('', include('transactions.urls')),
    path('', include('django.contrib.auth.urls')),
)

# Se combinan ambas tanto internacionalizadas como las que no, pero añadimos las no internacionalizadas al final
urlpatterns += urlpatterns_base

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)