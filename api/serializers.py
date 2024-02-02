from rest_framework import serializers
from clients.models import Account, CreditCard
from transactions.models import Transaction
# Recordar que los serializadores sirven para indicar el modelo y los campos a mostrar dentro del json de la api

# Tambien recordar importar en el settings.py rest_framework.renderers.JSONRenderer en el rest_framework para la visualizacion en json
# mirad aqui https://www.django-rest-framework.org/api-guide/renderers/
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'timestamp', 'amount', 'concept']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'code', 'alias', 'balance', 'status']

class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['id', 'card_code', 'alias', 'pin', 'status']
