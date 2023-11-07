from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import AccountRegistrationForm, AccountEditForm
from .models import Account
from django.utils.crypto import get_random_string


def register(request):
    if request.method == 'POST':
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            account = form.save()
            # Loguear al usuario automáticamente después de registrarse
            login(request, account)
            return redirect('dashboard')
    else:
        form = AccountRegistrationForm()
    return render(request, 'account/register.html', {'form': form})

@login_required
def edit_alias(request, account_id):
    # Obtener la cuenta actual
    account = get_object_or_404(Account, id=account_id)

    if request.method == 'POST':
        # Actualizar el alias de la cuenta
        new_alias = request.POST.get('new_alias')
        account.alias = new_alias

        # Guardar los cambios en la base de datos
        account.save()

        return redirect('dashboard')
    else:
        return render(request, 'account/edit_alias.html', {'account': account})

def logout_view(request):
    logout(request)
    return redirect('login')
from django.core.mail import send_mail
from django.contrib.auth import logout

@login_required
def deactivate_account(request):
    if request.method == 'POST':
        # Lógica para desactivar la cuenta del usuario
        account = request.user.account
        account.status = Account.Status.DOWN
        account.save()

        # Enviar el correo de reactivación
          # Generar un token de reactivación
        reactivation_token = get_random_string(length=32)
        account.reactivation_token = reactivation_token
        account.save()

        subject = 'Reactivate Your Account'
        message = f'Click the link to reactivate your account: http://localhost:8000/account/reactivate/{reactivation_token}'
        from_email = 'your_email@example.com'
        to_list = [request.user.email]

        send_mail(subject, message, from_email, to_list, fail_silently=True)

        logout(request)
        return redirect('login')
    return render(request, 'account/deactivate_account.html')

@login_required
def reactivate_account(request, token):
    # Lógica para reactivar la cuenta del usuario
    account = Account.objects.filter(reactivation_token=token, status=Account.Status.DOWN).first()
    if account:
        account.status = Account.Status.ACTIVE
        account.reactivation_token = None
        account.save()
        return render(request, 'account/reactivate_account.html', {'success': True})
    return render(request, 'account/reactivate_account.html', {'success': False})
