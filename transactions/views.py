from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from account.models import Account

from cards.models import CreditCard
from .models import Transaction

from transactions.forms import TransactionsForm
from .commisions import calcular_comision
import json

@login_required
def payment_form(request):
    if request.method == 'POST':
        form = TransactionsForm(request.POST)
        if form.is_valid():
            # Aquí puedes realizar cualquier acción necesaria con el formulario
            return redirect('process_payment')
    else:
        form = TransactionsForm()

    return render(request, 'payments/payment_form.html', {'form': form})

@csrf_exempt
def payment(request):
    if request.method == 'POST':
        # Obtener los datos del POST request
        data = json.loads(request.body)
        business = data.get('business')
        ccc = data.get('ccc')
        pin = data.get('pin')
        amount = data.get('amount')

        try:
            credit_card = CreditCard.objects.get(card_code=ccc)
        except CreditCard.DoesNotExist:
            return HttpResponseForbidden(f"Card '{ccc}' doesn't exist or doesn't match with any card")

        if not check_password(pin, credit_card.pin):
            return HttpResponseForbidden('The PIN code does not match')

        # Realizar el pago y actualizar el balance de la tarjeta
        comision = calcular_comision("salida", float(amount))
        credit_card.account.balance -= float(amount) + comision
        credit_card.account.save()

        # Crear registro de la transacción
        Transaction.objects.create(
            agent=business,
            concept="PAYMENT",
            amount=amount,
            kind='PAYMENT',
        )

        return HttpResponse("Ok!")
    else:
        return HttpResponseNotFound("Payment failed")

@csrf_exempt
def incoming(request):
    if request.method == 'POST':
        # Obtener los datos del POST request
        data = json.loads(request.body)
        # Lista de datos a recoger
        sender = data.get('sender')
        cac = data.get('cac')
        concept = data.get('concept')
        amount = data.get('amount')

        try:
            account = Account.objects.get(code=cac, status="AC")
        except Account.DoesNotExist:
            return HttpResponseForbidden(f"Account '{cac}' doesn't exist or is not active")

        # Realizar la transferencia y actualizar el balance de la cuenta
        comision = calcular_comision("entrada", float(amount))
        print(comision)
        print(amount)
        account.balance += float(amount) -comision
        account.save()

        # Crear la transacción
        Transaction.objects.create(
            agent=sender,
            amount=float(amount),
            kind='INCOMING',
            concept=concept
        )

        return HttpResponse("Ok!")
    else:
        return HttpResponseNotFound("Incoming transfer failed")
