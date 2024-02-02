import csv
import datetime
from decimal import Decimal
import json
import django
import requests  # Para realizar la solicitud POST a la otra entidad bancaria
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from clients.models import Account, CreditCard

from .commisions import calcular_comision
from .forms import PaymentForm, TransferForm
from .models import Transaction
from django.template.loader import render_to_string
from django.template import Context
from weasyprint import HTML


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
        ccc = data.get('ccc')  
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
            print()
            credit_card.account.balance -= amount + comision
            print(credit_card.account)
            credit_card.account.save()

            # Crear registro de la transacción
            Transaction.objects.create(
                agent=business,
                concept="PAYMENT",
                amount=amount + comision,
                kind='PAYMENT',
                account=credit_card.account,
            )

            return HttpResponse("Ok!")
        except django.db.utils.IntegrityError:
            return HttpResponseNotFound("You don't have enought money for the payment")
    else:
        accounts = Account.objects.filter(client=request.user.client)
        return render(request, 'payments/payment_form.html', {'accounts': accounts})

def generate_pdf(transaction):
    # Renderizar el contenido del PDF con la información de la transacción
    context = {'transaction': transaction}
    html_content = render_to_string('pdf/justificante_template.html', context)

    # Generar el PDF con WeasyPrint
    pdf_content = HTML(string=html_content).write_pdf()

    return pdf_content

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
        
        if account.balance < (amount + comision):
            return HttpResponse("Not enough money for the transfer")
    
        url_banks = 'https://raw.githubusercontent.com/sdelquin/dsw/main/ut3/te1/notes/files/banks.json'
        response = requests.get(url_banks)
        banks = response.json()
        for bank in banks:
            if bank.get("id") == int(cac[1]):
                url = bank.get("url")
        
        # Enviar la solicitud POST al banco 2 para registrar la transacción entrante
        bank2_url = url+":8000"+ "/transfer/incoming/"
        # bank2_url = "http://192.168.1.42:8000/transfer/incoming/"
        payload = {"sender": sender, "cac": cac, "concept": concept, "amount": str(amount)}
        response = requests.post(bank2_url, json=payload)
        print(bank2_url, payload)
        if response.status_code == 200:
            
            account.balance -= amount + comision
            account.save()
            transaction = Transaction.objects.create(
                agent=sender, amount=(amount + comision), kind='OUTGOING', concept=concept, account=account
            )

            # Generar el justificante en PDF
            pdf_content = generate_pdf(transaction)

            # Devolver el PDF como respuesta
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="justificante_{transaction.id}.pdf"'
            return response
        else:
            print(response.status_code)
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
        sender = data.get("sender")
        cac = data.get('cac')
        concept = data.get('concept')
        amount = data.get('amount')

        try:
            account = Account.objects.get(code=cac, status="AC")
        except Account.DoesNotExist:
            return HttpResponseForbidden(f"Account '{cac}' doesn't exist or is not active")

        # Realizar la transferencia y actualizar el balance de la cuenta
        comision = calcular_comision("entrada", Decimal(amount))
        account.balance += Decimal(amount) - comision
        account.save()

        # Crear la transacción
        Transaction.objects.create(
            agent=sender, amount=(Decimal(amount)- comision), kind='INCOMING', concept=concept , account=account
        )

        return HttpResponse("Ok!", status=200)
    else:
        return HttpResponseNotFound("Incoming transfer failed")


def movements(request):
    # Obtener todas las cuentas bancarias del usuario actual
    accounts = Account.objects.filter(client=request.user.client, status=Account.Status.ACTIVE)

    # Filtrado por cuenta
    account_id = request.GET.get('account_id', '')
    if account_id:
        transactions = Transaction.objects.filter(account__code=account_id)
    else:
        # Si no se especifica una cuenta, mostrar todas las transacciones del usuario
        transactions = Transaction.objects.filter(account__in=accounts)

    # Filtrado por tipo de transacción
    transaction_type = request.GET.get('transaction_type', '')
    if transaction_type:
        transactions = transactions.filter(kind=transaction_type)

    transactions = transactions.order_by('-timestamp')

    # Paginación
    paginator = Paginator(transactions, 5)
    page = request.GET.get('page', 1)
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    return render(request, 'transfers/movements.html', {'transactions': transactions, 'accounts': accounts})


# exportación de CSV
def export_transactions_csv(request):
    # Obtener el cliente actual del usuario
    current_client = request.user.client

    # Obtener la cuenta actual del cliente
    current_account = current_client.account_set.first()

    # Obtener solo las transacciones de la cuenta actual
    transactions = Transaction.objects.filter(account=current_account)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    writer = csv.writer(response)
    fields = ['kind', 'agent', 'concept', 'timestamp', 'amount']

    # Escribir la primera fila con la información del encabezado
    writer.writerow([Transaction._meta.get_field(field).verbose_name for field in fields])

    # Escribir las filas de datos
    for transaction in transactions:
        data_row = [getattr(transaction, field) for field in fields]
        # Convertir campos de fecha a formato legible
        for i, field in enumerate(fields):
            if isinstance(getattr(transaction, field), datetime.datetime):
                data_row[i] = getattr(transaction, field).strftime('%d/%m/%Y')
        writer.writerow(data_row)

    return response