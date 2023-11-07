from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect

from account.models import Account
from .models import CreditCard
from .forms import CreditCardForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password


# Lista para mostrar en el dashboard
@login_required
def credit_card_list(request):
    credit_cards = CreditCard.objects.all()
    return render(request, 'cards/credit_card_list.html', {'credit_cards': credit_cards})

# Para solo el apartado de tarjetas
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
    # Obtener la cantidad de tarjetas de crédito que el usuario ya tiene
    card_count = CreditCard.objects.filter(account__client=request.user.client).count()
    
    # Verificar si el usuario ya ha alcanzado el límite de tarjetas
    if card_count >= 4:
        messages.error(request, 'Has alcanzado el límite máximo de tarjetas de crédito.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CreditCardForm(request.user.client, request.POST)
        if form.is_valid():
            # Crear el nuevo objeto CreditCard
            credit_card = form.save(commit=False)
            
            # Asignar la cuenta del cliente a la tarjeta de crédito
            credit_card.account = form.cleaned_data['account']
            
            # Guardar el PIN en una variable antes de hashearla
            pin = credit_card.pin

            # Hashear el PIN
            credit_card.pin = make_password(pin)
            
            credit_card.save()

            # Enviar correo de éxito al usuario
            send_mail(
                'Tu tarjeta ha sido creada con éxito',
                f'Este es tu PIN: {pin}',
                'your_email@example.com',
                [request.user.email],
                fail_silently=False,
            )
            return redirect('cards:credit_cards')
    else:
        form = CreditCardForm(request.user.client)

    return render(request, 'cards/add_credit_card.html', {'form': form})

@login_required
def block_credit_card(request, card_code):
    # Obtener la tarjeta de crédito
    card = get_object_or_404(CreditCard, card_code=card_code)
    
    # Verificar si el usuario actual es el propietario de la tarjeta
    if card.account.client.user == request.user:
        if card.status == CreditCard.Status.BLOCK:
            messages.error(request, 'Esta tarjeta ya está bloqueada.')
            return redirect('home')
        # Bloquear la tarjeta
        card.status = CreditCard.Status.BLOCK
        card.save()
        
        # Enviar correo de confirmación de bloqueo
        send_mail(
            'Your credit card has been blocked',
            'Your credit card with code {} has been successfully blocked.'.format(card.card_code),
            'your_email@example.com',
            [card.account.client.user.email],
            fail_silently=True,
        )
        
        messages.success(request, 'Credit card blocked successfully')
        return redirect('home')
    else:
        messages.error(request, 'You are not authorized to block this credit card')
        return redirect('home')


@login_required
def delete_credit_card(request, card_code):
    card = get_object_or_404(CreditCard, card_code=card_code)
    if request.method == 'POST':
        card.delete()
        send_mail(
            'Your credit card has been deleted',
            'Your credit card with code {} has been successfully deleted.'.format(card.card_code),
            'your_email@example.com',
            [card.account.client.user.email],
            fail_silently=True,
        )
        messages.success(request, 'La tarjeta ha sido eliminada correctamente.')
        return redirect('home')
    else:
        return render(request, 'cards/confirm_delete_card.html', {'card': card})

