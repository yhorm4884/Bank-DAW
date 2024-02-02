from rest_framework import serializers
from clients.models import Account, CreditCard
from transactions.models import Transaction

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
