from django.urls import path, include
from rest_framework import routers
from . import views

#Rutas automáticas con router:
# Ruta	Descripción
# /api/accounts/	Listado de cuentas (del cliente autenticado)
# /api/accounts/<pk>/	Detalle de cuenta
# /api/transactions/	Listado de transacciones (del cliente autenticado)
# /api/transactions/<pk>/	Detalle de transacción
# /api/cards/	Listado de tarjetas (del cliente autenticado)
# /api/cards/<pk>/	Detalle de tarjeta
router = routers.DefaultRouter()
router.register('accounts', views.AccountViewSet)
router.register('transactions', views.TransactionViewSet)
router.register('cards', views.CreditCardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]