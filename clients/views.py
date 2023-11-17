from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.crypto import get_random_string

from account.models import Account
from cards.models import CreditCard
from clients.forms import (
    ClientEditForm,
    ClientRegistrationForm,
    LoginForm,
    UserEditForm,
    UserRegistrationForm,
)

from .models import Client


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        client_form = ClientRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and client_form.is_valid():
            # Save the user's data
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Save the client's data
            client = client_form.save(commit=False)
            client.user = user
            client.save()

            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        client_form = ClientRegistrationForm()
    return render(
        request, 'client/register.html', {'user_form': user_form, 'client_form': client_form}
    )


def client_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.client.status == 'AC':
                    login(request, user)
                    return redirect('home')
                elif user.client.status == 'DO':
                    messages.error(
                        request,
                        'Your account is inactive, please check your email to reactivate it',
                    )
                else:
                    messages.error(request, 'Account is blocked')
            else:
                messages.error(request, 'Invalid login')
    else:
        form = LoginForm(request=request)
    return render(request, 'client/login.html', {'form': form})


@login_required
def dashboard(request):
    # Obtener las cuentas del cliente
    print(request.user)
    accounts = Account.objects.filter(client=request.user.client)
    # Obtener las tarjetas de crédito asociadas a esas cuentas
    credit_cards = CreditCard.objects.filter(account__in=accounts)

    return render(
        request, 'client/dashboard.html', {'accounts': accounts, 'credit_cards': credit_cards}
    )


@login_required
def profile(request):
    profile = request.user.client
    return render(request, 'client/profile.html', {'profile': profile})


@login_required
def edit(request):
    if request.method == 'POST':
        client_form = ClientEditForm(
            instance=request.user.client, files=request.FILES, data=request.POST
        )
        print(request.FILES)
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if client_form.is_valid() and user_form.is_valid():
            client_form.save()
            user_form.save()
            messages.success(request, 'Profile updated successfully')
            return render(request, 'client/profile.html', {'profile': profile})
        else:
            messages.error(request, 'Error updating your profile')
    else:
        client_form = ClientEditForm(instance=request.user.client)
        user_form = UserEditForm(instance=request.user)
        photo = request.user.client

    return render(
        request,
        'client/edit.html',
        {'client_form': client_form, 'user_form': user_form, 'photo': photo},
    )


@login_required
def deactivate_account(request):
    # Obtener el usuario actual
    client = request.user.client

    # Cambiar el estado del usuario a 'Inactivo'
    client.status = 'DO'

    # Generar un token de reactivación
    reactivation_token = get_random_string(length=32)
    client.reactivation_token = reactivation_token

    # Guardar los cambios en la base de datos
    client.save()

    # Enviar el correo de reactivación
    subject = 'Reactivate Your Account'
    message = f'Click the link to reactivate your account: http://localhost:8000/client/reactivate/{reactivation_token}'
    from_email = 'your_email@example.com'
    to_list = [client.user.email]

    send_mail(subject, message, from_email, to_list, fail_silently=True)

    # Cerrar la sesión del cliente
    logout(request)

    # Redirigir al cliente a la página de inicio
    return redirect('home')


def reactivate_account(request, token):
    # Buscar un usuario con el token de reactivación proporcionado
    client = get_object_or_404(Client, reactivation_token=token)

    # Cambiar el estado del usuario a 'Activo'
    client.status = 'AC'

    # Eliminar el token de reactivación
    client.reactivation_token = None

    # Guardar los cambios en la base de datos
    client.save()

    # Iniciar sesión del cliente
    login(request, client.user)

    # Redirigir al cliente a la página de inicio
    return redirect('home')
