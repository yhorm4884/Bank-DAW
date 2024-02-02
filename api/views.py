from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .serializers import AccountSerializer, CreditCardSerializer, TransactionSerializer
from clients.models import CreditCard, Account
from transactions.models import Transaction
# Usar authentication_classes con sessionAuthentication para la utenticacion por sesión y get_queryset para tanto comprobar 
#que se utiliza el metodo get como que se comprueba el cliente actual de la cuenta y así no meternos en la cuenta de otra persona

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return self.queryset.filter(client=self.request.user.client)

class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return self.queryset.filter(account__client=self.request.user.client)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return self.queryset.filter(account__client=self.request.user.client)
