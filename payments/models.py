from django.db import models

class Payment(models.Model):
    business = models.CharField(max_length=100)
    ccc = models.CharField(max_length=20)
    pin = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
