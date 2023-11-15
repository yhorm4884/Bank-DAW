from django.db import models
from clients.models import Client
# ┌───────────────────────┐
# │   Transactions        │
# ├───────────────────────┤
# │  agent                │
# │  concept              │
# │  timestamp            │
# │  amount               │
# │  kind                 │
# └───────────────────────┘

class Transaction(models.Model):
    KIND_CHOICES = [
        ('INCOMING', 'Incoming Transfer'),
        ('OUTGOING', 'Outgoing Transfer'),
        ('PAYMENT', 'Payment'),
    ]

    agent = models.CharField(max_length=20)
    concept = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    #client  = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f'{self.kind} - {self.agent} - {self.amount}'