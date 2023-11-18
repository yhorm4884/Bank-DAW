from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from clients.models import Client

# ┌───────────────────────┐
# │   Account             │
# ├───────────────────────┤
# │  code                 │
# │  alias                │
# │  balance              │
# │  status               │
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
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    # Campo extra que servirá para cuando la cuenta esté desactivada
    reactivation_token = models.CharField(max_length=64, null=True, blank=True)

    # Balance que dice el total de dinero en la cuenta del banco
    balance = models.DecimalField(decimal_places=2, max_digits=6, validators=[MinValueValidator(0)], null=True,default=0)


    # Estado en el que se encuentra la cuenta actualmente
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)
    def save(self, *args, **kwargs):
        # Si no se ha asignado un code, generar uno
        if not self.code:
            # Obtener la última cuenta
            last_account = Account.objects.order_by('-code').first()
            if last_account:
                last_code = last_account.code
                last_num = int(last_code.split('-')[1])
                new_num = last_num + 1
                new_code = f"A2-{new_num:04d}"
            else:
                new_code = "A2-0001"

            self.code = new_code
        # Llamar al método save() del padre
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.alias}/{self.code}'
