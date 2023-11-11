import json

from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from account.models import Account

from .forms import TransferForm


@csrf_exempt
def incoming(request):
    if request.method == 'POST':
        # Obtener los datos del POST request
        data = json.loads(request.body)
        sender = data.get('sender')
        cac = data.get('cac')
        concept = data.get('concept')
        amount = data.get('amount')

        # print(business,ccc,pin,amount)
        print(data)
        try:
            cuenta = Account.objects.get(code=cac, status="AC")
            print(cuenta)
        except Account.DoesNotExist:
            # Envio 404 porque no existe la tarjeta
            return HttpResponseForbidden(f"Account '{cac} doesn't exists '")

        # Realizar el pago y actualizar el balance de la tarjeta
        print(cuenta.balance)
        cuenta.balance += float(amount)

        cuenta.save()
        return HttpResponse("{200} Ok!")
    else:
        return HttpResponseNotFound("La transferencia ha sido un éxito")

@login_required
def transfer_form(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            
           
    else:
        form = TransferForm()
    return render(request, 'payments/payment_form.html', {'form': form})
