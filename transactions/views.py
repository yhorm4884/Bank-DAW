import json

import django
import requests  # Para realizar la solicitud POST a la otra entidad bancaria
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)
from django.core.exceptions import FieldError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from account.models import Account
from cards.models import CreditCard

from .commisions import calcular_comision
from .forms import PaymentForm, TransferForm
from .models import Transaction


@login_required
@csrf_exempt
def payment(request):
    if request.method == 'POST':
        # Obtener los datos del POST request
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            form = PaymentForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
            else:
                return HttpResponseForbidden(f"Invalid form data format")
        business = data.get('business')
        ccc = data.get('ccc')  # C2-0001
        pin = data.get('pin')
        amount = data.get('amount')

        try:
            credit_card = CreditCard.objects.get(card_code=ccc)
        except CreditCard.DoesNotExist:
            return HttpResponseForbidden(
                f"Card '{ccc}' doesn't exist or doesn't match with any card"
            )

        if not check_password(pin, credit_card.pin):
            return HttpResponseForbidden('The PIN code does not match')
        try:
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
        except django.db.utils.IntegrityError:
            return HttpResponseNotFound("You don't have enought money for the payment")
    else:
        accounts = Account.objects.filter(client=request.user.client)
        return render(request, 'payments/payment_form.html', {'accounts': accounts})



@login_required
@csrf_exempt
def outcoming(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            form = TransferForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
            else:
                return HttpResponseForbidden(f"Invalid form data format")
        sender = data.get('sender')
        cac = data.get('cac')
        concept = data.get('concept')
        amount = data.get('amount')
        # print(data, sender, cac, concept)
        # Comprobar si la cuenta (cac) existe en la base de datos
        try:
            account = Account.objects.get(code=cac, status="AC")
        except Account.DoesNotExist:
            # Si la cuenta no existe en la base de datos, usar la cuenta actual del usuario
            selected_account_alias = data.get('sender')
            account = get_object_or_404(Account, alias=selected_account_alias, client=request.user.client)            
        comision = calcular_comision("salida", float(amount))
        
        if account.balance < (float(amount) + comision):
            return HttpResponse("Not enough money for the transfer")
    
        url_banks = 'https://raw.githubusercontent.com/sdelquin/dsw/main/ut3/te1/files/banks.json'
        response = requests.get(url_banks)
        banks = response.json()
        for bank in banks:
            if bank.get("id") == int(cac[1]):
                url = bank.get("url")

        # Enviar la solicitud POST al banco 2 para registrar la transacción entrante
        bank2_url = url+":8000"+ "/transfer/incoming/"
        payload = {"sender": sender, "cac": cac, "concept": concept, "amount": str(amount)}
        print(bank2_url)
        response = requests.post(bank2_url, json=payload)
        if response.status_code == 200:
            account.balance -= float(amount) + comision
            account.save()
            Transaction.objects.create(
                agent=sender, amount=float(amount), kind='OUTGOING', concept=concept, account=account
            )
            return HttpResponse("Transaction completed successfully")
        else:
            return HttpResponse({"Transaction to bank failed"})
    else:
        accounts = Account.objects.filter(client=request.user.client)

        return render(request, 'transfers/transfers_form.html', {'accounts': accounts})


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
        account.balance += float(amount) - comision
        account.save()

        # Crear la transacción
        Transaction.objects.create(
            agent=sender, amount=float(amount), kind='INCOMING', concept=concept , account=account
        )

        return HttpResponse("Ok!", status=200)
    else:
        return HttpResponseNotFound("Incoming transfer failed")


@login_required
def transactions(request):
    accounts = Account.objects.filter(client=request.user.client, status=Account.Status.ACTIVE)

    return render(request, 'transfers/select_account.html', {'accounts': accounts})


@login_required
def transactions_list(request, account=str):
    account = Account.objects.get(code=account, status=Account.Status.ACTIVE)
    transferencia = Transaction.objects.filter(account=account)
    print("---------------", transferencia)

    # if accounts:
    #     transactions = Transaction.objects.filter(account=accounts)
    # else:
    #     transactions = Transaction.objects.none()

    return render(request, 'transfers/list.html', {'transactions': transferencia})
