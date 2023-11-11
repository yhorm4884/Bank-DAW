from django.db import models

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
    AGENT_CHOICES = [
        ('bank', 'Bank'),
        ('business', 'Business'),
        ('client', 'Client'),
    ]

    KIND_CHOICES = [
        ('incoming', 'Incoming Transfer'),
        ('outgoing', 'Outgoing Transfer'),
        ('payment', 'Payment'),
    ]

    agent = models.CharField(max_length=20, choices=AGENT_CHOICES)
    concept = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)

    def __str__(self):
        return f'{self.kind} - {self.agent} - {self.amount}'