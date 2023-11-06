from django.conf import settings
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models

# ┌───────────────────────┐
# │   Account             │
# ├───────────────────────┤
# │  code                 │
# │  alias                │
# │  balance              │
# │  status               │
# │  avatar               │
# └───────────────────────┘

# TODO Falta añadir balance que no sé sabe por ahora lo que es
class Account(models.Model):
    # Formateo para el codigo de cuenta
    formato_regex = r'^A2-\d{4}$'
    # Creación de la clase de elección entre activo, bloqueado o de baja
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Activo'
        BLOCK = 'BL', 'Bloqueado'
        DOWN = 'DO', 'Inactivo'
    # Codigo autoincrementar que va a permitir indentificar la cuenta
    code = models.CharField(
        unique=True, max_length=7, validators=[RegexValidator(regex=formato_regex)]
    )
    alias = models.CharField(max_length=255)
    # Datos del cliente ya que un cliente puede tener muchas cuentas
    client = models.ForeignKey('client', on_delete=models.CASCADE)

    # Campo extra que servirá para cuando la cuenta esté desactivada
    reactivation_token = models.CharField(max_length=64, null=True, blank=True)

    # Balance que dice el total de dinero en la cuenta del banco
    balance = models.PositiveIntegerField()

    # Avatar que puede mostrar el usuario en la web
    # TODO Si es posible en un futuro implementar upload to accounts/code estaría bien
    avatar = models.ImageField(
        upload_to='accounts/%Y/%m/%d/', blank=True, validators=[FileExtensionValidator(['jpg', 'png'])]
    )

    # Estado en el que se encuentra la cuenta actualmente
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return f'Bienvenido a la cuenta {self.alias}, código: {self.code}'
