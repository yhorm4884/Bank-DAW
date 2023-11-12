from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

# ┌───────────────────────┐
# │   Clients             │
# ├───────────────────────┤
# │  username             │
# │  first_name           │
# │  last_name            │
# │  email                │
# │  password             │
# │  status               │
# │  avatar               │
# └───────────────────────┘


# TODO Falta añadir balance que no sé sabe por ahora lo que es
class Client(models.Model):
    # Creación de la clase de elección entre activo, bloqueado o de baja
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Activo'
        BLOCK = 'BL', 'Bloqueado'
        DOWN = 'DO', 'Inactivo'

    # Campo OnetoOne que sirve para hacer referencia al
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)

    # Campo extra que servirá para cuando la cuenta esté desactivada
    reactivation_token = models.CharField(max_length=64, null=True, blank=True)

    # Estado en el que se encuentra la cuenta actualmente
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)
    photo = models.ImageField(
        upload_to='client/%Y/%m/%d/',
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'png'])],
    )

    def __str__(self):
        return f'{self.user.username}'
