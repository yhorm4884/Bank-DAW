from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AccountRegistrationForm, AccountEditForm, AddMoneyForm
from .models import Account
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate

@login_required
def register(request):
    if request.method == 'POST':
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            # Verifica si la contraseña ingresada es correcta
            user = authenticate(username=request.user.username, password=form.cleaned_data['password'])
            if user is not None:
                # La contraseña es correcta, crea la nueva cuenta
                account = form.save(commit=False)
                account.client = request.user.client
                account.save()

                return redirect('home')
            else:
                # La contraseña no es correcta, muestra un mensaje de error
                messages.error(request, 'La contraseña actual ingresada no es correcta.')
    else:
        form = AccountRegistrationForm()
    return render(request, 'account/register.html', {'form': form})

@login_required
def accounts(request):
    # Obtener todas las cuentas del cliente
    accounts = Account.objects.filter(client=request.user.client, status=Account.Status.ACTIVE)
    # Pasar las cuentas al contexto de la plantilla
    return render(request, 'account/accounts.html', {'accounts': accounts})

@login_required
def account_details(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    credit_cards = account.credit_cards.all()
    # print(credit_cards)
    return render(request, 'account/account_details.html', {'account': account, 'credit_cards': credit_cards})

@login_required
def add_money(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    if request.method == 'POST':
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            # Obtener el monto a añadir
            amount = form.cleaned_data['amount']

            # Realizar la operación de agregar dinero
            account.balance += amount
            account.save()

            # Mensaje de éxito
            messages.success(request, f'Se han añadido {amount} euros a la cuenta {account.alias}. Balance actual: {account.balance} euros.')

            # Redirigir al usuario a la página de detalles de la cuenta
            return redirect('account:account_details', account_id=account.id)
    else:
        form = AddMoneyForm()

    return render(request, 'account/add_money.html', {'form': form, 'account': account})    
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

        # Mostrar un mensaje de éxito
        messages.success(request, 'El alias de la cuenta se ha cambiado correctamente.')

        # Redirigir al usuario a la página de cuentas
        return redirect('home')
    else:
        return render(request, 'account/edit_alias.html', {'account': account})

@login_required
def deactivate_account(request,account_id):
    if request.method == 'POST':
        # Obtener la cuenta específica que deseas desactivar
        account = get_object_or_404(Account, id=account_id, client=request.user.client)
        # Comprobar si la cuenta ya está desactivada
        if account.status == Account.Status.BLOCK:
            messages.warning(request, 'La cuenta ya está desactivada.')
            return redirect('home')
        # Cambiar el estado de la cuenta a 'BLOCKEADO'
        account.status = Account.Status.BLOCK
        account.save()
        # Generar un token de reactivación
        reactivation_token = get_random_string(length=32)
        account.reactivation_token = reactivation_token
        account.save()

        subject = 'Reactivate Your Account'
        message = f'Click the link to reactivate your account: http://localhost:8000/account/reactivate/{reactivation_token}'
        from_email = 'your_email@example.com'
        to_list = [request.user.email]

        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('home')
    return render(request, 'account/deactivate_account.html')

@login_required
def reactivate_account(request, token):
    # Lógica para reactivar la cuenta del usuario
    account = Account.objects.filter(reactivation_token=token, status=Account.Status.BLOCK).first()
    if account:
        account.status = Account.Status.ACTIVE
        account.reactivation_token = None
        account.save()
        return render(request, 'account/reactivate_account.html', {'success': True})
    return render(request, 'account/reactivate_account.html', {'success': False})
