import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound

from bank.commisions import calcular_comision
from .forms import PaymentForm
from django.http import JsonResponse
from cards.models import CreditCard
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt

def payment_form(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            return redirect('payments:process_payment')
    else:
        form = PaymentForm()
    return render(request, 'payments/payment_form.html', {'form': form})

#Pago mediante el curl
@csrf_exempt
def payment(request):
    if request.method == 'POST':
        # Obtener los datos del POST request
        data = json.loads(request.body)
        business = data.get('business')
        ccc = data.get('ccc')
        pin = data.get('pin')
        amount = data.get('amount')
        
        # print(business,ccc,pin,amount)
        try:
            credit_card = CreditCard.objects.get(card_code=ccc)
        except CreditCard.DoesNotExist:
            #Envio 404 porque no existe la tarjeta
            return HttpResponseForbidden(f"Card '{ccc} doesn't exists doesn't match with any card'")
        if not check_password(pin, credit_card.pin):
            return HttpResponseForbidden('The code pin does not match')

        # Realizar el pago y actualizar el balance de la tarjeta
        
        comision = calcular_comision("pago", float(amount))
        print(comision)
        credit_card.account.balance += float(amount) - comision
        print(credit_card.account.balance)

        credit_card.account.save()
        return HttpResponse("Ok!")
    else:
        return HttpResponseNotFound("El pago ha fallado")