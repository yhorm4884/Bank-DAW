
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


from . import views

urlpatterns = [
    path('login/', views.client_login, name='login'),
    path('register/', views.register, name='client_register'),
    path('', views.dashboard, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('deactivate/', views.deactivate_account, name='deactivate'),
    path('reactivate/<str:token>/', views.reactivate_account, name='reactivate'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

