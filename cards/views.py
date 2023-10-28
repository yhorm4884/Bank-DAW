from django.shortcuts import render, redirect
from .models import CreditCard
from .forms import CreditCardForm

def credit_card_list(request):
    cards = CreditCard.objects.all()
    return render(request, 'cards/credit_card_list.html', {'cards': cards})

from django.shortcuts import render, redirect
from .forms import CreditCardForm
from .models import CreditCard

def add_credit_card(request):
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


