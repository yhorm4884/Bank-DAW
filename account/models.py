from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Profile(models.Model):
    # Creación de la clase de elección entre activo, bloqueado o de baja
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Activo'
        BLOCK = 'BL', 'Bloqueado'
        DOWN = 'DO', 'Inactivo'

    # Formateo para el codigo de cuenta
    formato_regex = r'^A2-\d{4}$'

    # Datos del usuario como nombre, apellidos, correo...
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Avatar que puede mostrar el usuario en la web
    # TODO Si es posible en un futuro implementar upload to user/code estaría bien
    avatar = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    # Codigo autoincrementar que va a permitir indentificar la cuenta
    code = models.CharField(
        unique=True, max_length=7, validators=[RegexValidator(regex=formato_regex)]
    )
    # Estado en el que se encuentra la cuenta actualmente
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return f'Perfil de {self.user.username}, código: {self.code}'
