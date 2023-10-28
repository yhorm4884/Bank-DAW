from django.db import models
from django.conf import settings
import random
import string
from django.core.validators import RegexValidator

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_cards')
