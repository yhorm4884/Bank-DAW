from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from .models import CreditCard
from .forms import CreditCardForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Lista para mostrar en el dashboard
@login_required
def credit_card_list(request):
    credit_cards = CreditCard.objects.all()
    return render(request, 'cards/credit_card_list.html', {'credit_cards': credit_cards})

# Para solo el apartado de tarjetas
@login_required
def credit_cards(request):
    status = request.GET.get('status')
    if status:
        credit_cards = CreditCard.objects.filter(user=request.user, status=status)
    else:
        credit_cards = CreditCard.objects.filter(user=request.user)
    return render(request, 'cards/credit_cards.html', {'credit_cards': credit_cards})

@login_required
def add_credit_card(request):
    # Obtener la cantidad de tarjetas de crédito que el usuario ya tiene
    card_count = CreditCard.objects.filter(user=request.user).count()
    
    # Verificar si el usuario ya ha alcanzado el límite de tarjetas
    if card_count >= 4:
        messages.error(request, 'Has alcanzado el límite máximo de tarjetas de crédito.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            # Crear el nuevo objeto CreditCard
            credit_card = form.save(commit=False)
            
            # Asignar el usuario actual
            credit_card.user = request.user
            
            credit_card.save()
            return redirect('dashboard')
    else:
        form = CreditCardForm()

    return render(request, 'cards/add_credit_card.html', {'form': form})


def block_credit_card(request, card_code):
    # Obtener la tarjeta de crédito
    card = get_object_or_404(CreditCard, card_code=card_code)
    
    # Verificar si el usuario actual es el propietario de la tarjeta
    if card.user == request.user:
        if card.status == CreditCard.Status.BLOCK:
            messages.error(request, 'Esta tarjeta ya está bloqueada.')
            return redirect('cards:credit_cards')
        # Bloquear la tarjeta
        card.status = CreditCard.Status.BLOCK
        card.save()
        
        # Enviar correo de confirmación de bloqueo
        send_mail(
            'Your credit card has been blocked',
            'Your credit card with code {} has been successfully blocked.'.format(card.card_code),
            'your_email@example.com',
            [card.user.email],
            fail_silently=True,
        )
        
        messages.success(request, 'Credit card blocked successfully')
        return redirect('cards:credit_cards')
    else:
        messages.error(request, 'You are not authorized to block this credit card')
        return redirect('cards:credit_cards')

@login_required
def delete_credit_card(request, card_code):
    card = get_object_or_404(CreditCard, card_code=card_code)
    if request.method == 'POST':
        card.delete()
        send_mail(
            'Your credit card has been deleted',
            'Your credit card with code {} has been successfully deleted.'.format(card.card_code),
            'your_email@example.com',
            [card.user.email],
            fail_silently=True,
        )
        messages.success(request, 'La tarjeta ha sido eliminada correctamente.')
        return redirect('cards:credit_cards')
    else:
        return render(request, 'cards/confirm_delete_card.html', {'card': card})
