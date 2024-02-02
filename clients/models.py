import random
import string
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator,FileExtensionValidator, RegexValidator

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

# Cuentas

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

# Tarjeta Credito

# ┌───────────────────────┐
# │   card                │
# │                       │
# ├───────────────────────┤
# │  code                 │
# │  alias                │
# │  pin                  │
# │  status               │
# └───────────────────────┘

#Generador de secuencias de 3 caracteres alfanuméricos
def generate_pin():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))

class CreditCard(models.Model):
    #Como en la cuenta se recrea un estado de la tarjeta

    # TODO Buscar alternativa o opcion si al final borramos la tarjeta o solamente la bloqueamos
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Activa'
        BLOCK = 'BL', 'Bloqueada'
        DOWN = 'DO', 'Inactiva'
    #Expresión regular para el código de la tarjeta
    formato_regex = r'^C2-\d{4}$'

    #Campos        
    card_code = models.CharField(max_length=7, unique=True, validators=[RegexValidator(regex=formato_regex)])
    pin = models.CharField(max_length=3, default=generate_pin)
    alias = models.CharField(max_length=255)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)

    # Este campo es provisional ya que hay que establezcer una relación de clave foránea con el modelo User
    # para asi las tarjetas estén asociadas a una cuenta 
    account  = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='credit_cards')
    def save(self, *args, **kwargs):
        # Si no se ha asignado un card_code, generar uno
        if not self.card_code:
            # Obtener el último código
            last_credit_card = CreditCard.objects.order_by('-card_code').first()
            if last_credit_card:
                last_code = last_credit_card.card_code
                last_num = int(last_code.split('-')[1])
                new_num = last_num + 1
                new_code = f"C2-{new_num:04d}"
            else:
                new_code = "C2-0001"

            self.card_code = new_code
        # Llamar al método save() del padre
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.card_code}'
    