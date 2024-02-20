import json
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from .forms import AccountRegistrationForm, AddMoneyForm, ClientEditForm, ClientRegistrationForm, CreditCardForm, CreditCardFormWithoutAccount, LoginForm, UserEditForm, UserRegistrationForm
from .models import Account, Client, CreditCard 
from transactions.models import Transaction

#######################################################



# Cuentas

@login_required
def register(request):
    current_account_count = Account.objects.filter(client=request.user.client).count()
    if current_account_count >= 3:
        messages.error(request,  _('Número máximo de cuentas excedido (máximo 3 cuentas).'))
        return redirect('home')

    if request.method == 'POST':
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.username, password=form.cleaned_data['password'])
            if user is not None:
                account = form.save(commit=False)
                account.client = request.user.client
                account.save()
                return redirect('home')
            else:
                messages.error(request, _('La contraseña actual ingresada no es correcta.'))
    else:
        form = AccountRegistrationForm()

    return render(request, 'account/register.html', {'form': form})

@login_required
def accounts(request):
    accounts = Account.objects.filter(client=request.user.client, status=Account.Status.ACTIVE)
    return render(request, 'account/accounts.html', {'accounts': accounts})

@login_required
def account_details(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')
    credit_cards = account.credit_cards.all()
    return render(request, 'account/account_details.html', {'account': account,'transactions': transactions, 'credit_cards': credit_cards})

@login_required
def add_money(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if request.method == 'POST':
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount <= 1000000:
                if account.balance < 999999999.99:
                    account.balance += amount
                    account.save()
                else:
                    form.add_error('amount', _('La cantidad que ha puesto excede el límite que puede alvergar la cuenta.'))
                alias=account.alias
                balance=account.balance
                messages.success(request, _(f'Se han añadido {amount} euros a la cuenta {alias}. Balance actual: {balance} euros.'))
                return redirect('clients:account_details', account_id=account.id)
            else:
                form.add_error('amount', _('La cantidad no puede superar 1 millón de euros.')) 
    else:
        form = AddMoneyForm()

    return render(request, 'account/add_money.html', {'form': form, 'account': account})  
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
            messages.success(request, _('¡ Perfil actualizado correctamente !'))
            return render(request, 'client/profile.html', {'profile': profile})
        else:
            messages.error(request, _('Error al actualizar tu perfil'))
    else:
        client_form = ClientEditForm(instance=request.user.client)
        user_form = UserEditForm(instance=request.user)
        print("\n\n\n\n\n\n\n\n\n   ",request.user.client)
        photo = request.user.client

    return render(
        request,
        'client/edit.html',
        {'client_form': client_form, 'user_form': user_form, 'photo': photo},
    )

@login_required
def edit_alias(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    if request.method == 'POST':
        new_alias = request.POST.get('new_alias')
        account.alias = new_alias
        account.save()
        messages.success(request, _('El alias de la cuenta se ha cambiado correctamente.'))
        return redirect('home')
    else:
        return render(request, 'account/edit_alias.html', {'account': account})

@login_required
def deactivate_account(request, account_id):
    if request.method == 'POST':
        account = get_object_or_404(Account, id=account_id, client=request.user.client)

        if account.status == Account.Status.BLOCK:
            messages.warning(request, _('La cuenta ya está desactivada.'))
            return redirect('home')

        account.status = Account.Status.BLOCK
        account.save()

        reactivation_token = get_random_string(length=32)
        account.reactivation_token = reactivation_token
        account.save()

        subject = _('Reactiva tu cuenta')
        message = _(f'Pulsa en el enlace para reactivar tu cuenta: http://localhost:8000/es/reactivate/{reactivation_token}')
        from_email = 'your_email@example.com'
        to_list = [request.user.email]

        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('home')

    return render(request, 'account/deactivate_account.html')

@login_required
def reactivate_account(request, token):
    account = Account.objects.filter(reactivation_token=token, status=Account.Status.BLOCK).first()
    
    if account:
        account.status = Account.Status.ACTIVE
        account.reactivation_token = None
        account.save()
        return render(request, 'account/reactivate_account.html', {'success': True})
    
    return render(request, 'account/reactivate_account.html', {'success': False})




#######################################################




# Tarjetas

@login_required
def credit_card_list(request):
    credit_cards = CreditCard.objects.all()
    return render(request, 'cards/credit_card_list.html', {'credit_cards': credit_cards})

@login_required
def credit_cards(request):
    account_id = request.GET.get('account_id')
    status = request.GET.get('status')

    accounts = Account.objects.filter(client=request.user.client)

    if account_id:
        credit_cards = CreditCard.objects.filter(account_id=account_id, status=status)
    else:
        credit_cards = CreditCard.objects.none()

    return render(request, 'cards/credit_cards.html', {'credit_cards': credit_cards, 'accounts': accounts})

@login_required
def add_credit_card(request):
    card_count = CreditCard.objects.filter(account__client=request.user.client).count()
    
    if card_count >= 4:
        messages.error(request, _('Has alcanzado el límite máximo de tarjetas de crédito.'))
        return redirect('clients:home')

    if request.method == 'POST':
        form = CreditCardForm(request.user.client, request.POST)
        if form.is_valid():
            credit_card = form.save(commit=False)
            credit_card.account = form.cleaned_data['account']
            pin = credit_card.pin
            credit_card.pin = make_password(pin)
            credit_card.save()
            codigo=credit_card.card_code

            send_mail(
                _(f'Tu tarjeta {codigo} ha sido creada con éxito'),
                _(f'Este es tu PIN: {pin}'),
                'your_email@example.com',
                [request.user.email],
                fail_silently=False,
            )
            return redirect('clients:credit_cards')
    else:
        form = CreditCardForm(request.user.client)

    return render(request, 'cards/add_credit_card.html', {'form': form})

@login_required
def add_credit_card_without_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    card_count = CreditCard.objects.filter(account=account).count()

    if card_count >= 4:
        messages.error(request, _('Has alcanzado el límite máximo de tarjetas de crédito.'))
        return redirect('home')

    if request.method == 'POST':
        form = CreditCardFormWithoutAccount(request.POST)
        if form.is_valid():
            credit_card = form.save(commit=False)
            credit_card.account = account
            pin = credit_card.pin
            credit_card.pin = make_password(pin)
            credit_card.save()
            codigo =credit_card.card_code
            send_mail(
                _(f'Tu tarjeta {codigo} ha sido creada con éxito'),
                _(f'Este es tu PIN: {pin}'),
                'your_email@example.com',
                [request.user.email],
                fail_silently=True,
            )
            messages.success(request, _("Se ha creado la tarjeta con éxito"))
            return redirect('clients:account_details', account_id=account.id)
    else:
        form = CreditCardFormWithoutAccount()

    return render(request, 'cards/add_credit_card.html', {'form': form})

@login_required
def block_credit_card(request, card_code):
    card = get_object_or_404(CreditCard, card_code=card_code)
    
    if card.account.client.user == request.user:
        if card.status == CreditCard.Status.BLOCK:
            messages.error(request, _('Esta tarjeta ya está bloqueada.'))
            return redirect('home')

        card.status = CreditCard.Status.BLOCK
        card.save()

        send_mail(
            _('Tu tarjeta ha sido bloqueada'),
            _('Su tarjeta de crédito con código {} ha sido bloqueada exitosamente.'.format(card.card_code)),
            'your_email@example.com',
            [card.account.client.user.email],
            fail_silently=True,
        )
        
        messages.success(request, _('Tarjeta de crédito bloqueada exitosamente'))
        return redirect('home')
    else:
        messages.error(request, _('No estás autorizado a bloquear esta tarjeta de crédito'))
        return redirect('home')
@login_required
def reactivate_credit_card(request, card_code):
    card = get_object_or_404(CreditCard, card_code=card_code)

    if card.account.client.user == request.user:
        if card.status == CreditCard.Status.ACTIVE:
            messages.error(request, _('Esta tarjeta ya está activa.'))
            return redirect('home')

        card.status = CreditCard.Status.ACTIVE
        card.save()

        send_mail(
            _('Su tarjeta de crédito ha sido reactivada',),
            _('Su tarjeta de crédito con código {} ha sido reactivada exitosamente.'.format(card.card_code)),
            'your_email@example.com',
            [card.account.client.user.email],
            fail_silently=True,
        )

        messages.success(request, _('Tarjeta reactivada correctamente'))
        return redirect('home')
    else:
        messages.error(request, _('No estás autorizado para reactivar esta tarjeta de crédito.'))
        return redirect('home')
    
@login_required
def delete_credit_card(request, card_code):
    card = get_object_or_404(CreditCard, card_code=card_code)
    
    if request.method == 'POST':
        card.delete()

        send_mail(
            _('Su tarjeta de crédito ha sido eliminada'),
            _('Su tarjeta de crédito con código {} ha sido eliminada exitosamente.'.format(card.card_code)),
            'your_email@example.com',
            [card.account.client.user.email],
            fail_silently=True,
        )

        messages.success(request, _('La tarjeta ha sido eliminada correctamente.'))
        return redirect('home')
    else:
        return render(request, 'cards/confirm_delete_card.html', {'card': card})


#######################################################



# Clientes

def client_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        client_form = ClientRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            client = client_form.save(commit=False)
            client.user = user
            client.save()

            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        client_form = ClientRegistrationForm()

    return render(request, 'client/register.html', {'user_form': user_form, 'client_form': client_form})

def client_login(request):
    if request.method == 'POST':
        if request.user.is_authenticated and not request.user.is_superuser:
            return redirect('home')
        else:
            print("entro")
            form = LoginForm(request.POST, request=request)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(request, username=cd['username'], password=cd['password'])
                if user is not None and not user.is_superuser:
                    if user.client.status == 'AC':
                        login(request, user)
                        return redirect('home')
                    elif user.client.status == 'DO':
                        messages.error(request, _('Tu cuenta está inactiva, por favor revisa tu correo electrónico para reactivarla'))
                    else:
                        messages.error(request, _('La cuenta está bloqueada'))
                else:
                    messages.error(request, _('Inicio de sesión no válido o acceso denegado'))
    else:
        if request.user.is_superuser:
            logout(request)
        form = LoginForm(request=request)
    
    return render(request, 'client/login.html', {'form': form})



def dashboard(request):
    if request.user.is_superuser:
        logout(request)
        return render(request, 'extra/extras.html')
    elif request.user.is_authenticated:
       # Obtener el cliente actual
        client = request.user.client

        # Obtener cuentas asociadas al cliente
        accounts = Account.objects.filter(client=client)
        accounts_json = json.dumps([{'code': account.code, 'alias': account.alias} for account in accounts])
        print("Cuentas del cliente:", accounts_json)

        # Obtener tarjetas de crédito asociadas al cliente
        credit_cards = CreditCard.objects.filter(account__client=client)
        credit_cards_json = json.dumps([{'card_code': card.card_code, 'alias': card.alias} for card in credit_cards])
        print("Tarjetas de crédito del cliente:", credit_cards_json)

        # Obtener transacciones asociadas a las cuentas del cliente
        transactions = Transaction.objects.filter(account__client=client)
        transactions_json = json.dumps([{'id': transaction.id, 'agent': transaction.agent, 'amount': str(transaction.amount)} for transaction in transactions])
        print("Transacciones del cliente:", transactions_json)

        return render(request, 'client/dashboard.html', {
            'accounts': accounts,
            'accounts_json': accounts_json,
            'credit_cards': credit_cards,
            'credit_cards_json': credit_cards_json,
            'transactions': transactions,
            'transactions_json': transactions_json,
        })
    else:
        return render(request, 'extra/extras.html')

@login_required
def profile(request):
    profile = request.user.client
    return render(request, 'client/profile.html', {'profile': profile})

@login_required
def edit(request):
    if request.method == 'POST':
        client_form = ClientEditForm(instance=request.user.client, files=request.FILES, data=request.POST)
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if client_form.is_valid() and user_form.is_valid():
            client_form.save()
            user_form.save()
            messages.success(request, _('Perfil actualizado con éxito'))
            profile = request.user.client
            return render(request, 'client/profile.html', {'profile': profile})
        else:
            messages.error(request, _('Error al actualizar tu perfil'))
    else:
        client_form = ClientEditForm(instance=request.user.client)
        user_form = UserEditForm(instance=request.user)
        # photo = request.user.client.photo
        profile = request.user.client

    return render(request, 'client/edit.html', {'client_form': client_form, 'user_form': user_form, 'photo': profile.photo})

@login_required
def deactivate_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.status = 'DO'
    reactivation_token = get_random_string(length=32)
    client.reactivation_token = reactivation_token
    client.save()

    subject = _('Reactiva tu cuenta')
    message = _(f'Haga clic en el enlace para reactivar su cuenta: http://localhost:8000/client/reactivate/{reactivation_token}')
    from_email = 'your_email@example.com'
    to_list = [client.user.email]

    send_mail(subject, message, from_email, to_list, fail_silently=True)

    logout(request)
    return redirect('home')

def reactivate_client(request, token):
    client = get_object_or_404(Client, reactivation_token=token)
    client.status = 'AC'
    client.reactivation_token = None
    client.save()

    login(request, client.user)
    return redirect('home')