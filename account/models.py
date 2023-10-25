# Create your models here.
from django.conf import settings
from django.db import models


class Profile(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        BLOCK = 'BL', 'Block'
        DOWN = 'DO', 'Down'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)


def __str__(self):
    return f'Profile of {self.user.username}'
