# Create your models here.
from django.db import models


class Transfer(models.Model):
    sender = models.CharField(max_length=100)
    cac = models.CharField(max_length=20)
    concept = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
