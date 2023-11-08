from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PaymentForm
from django.http import JsonResponse
from cards.models import CreditCard
from django.contrib.auth.hashers import check_password


def payment_form(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            return redirect('payments:process_payment')
    else:
        form = PaymentForm()
    return render(request, 'payments/payment_form.html', {'form': form})

def payment(request):
    if request.method == 'POST':
        # Obtener los datos del POST request
        data = request.POST
        business = data.get('business')
        ccc = data.get('ccc')
        pin = data.get('pin')
        amount = data.get('amount')

        # Validar que los campos no estén vacíos
        if not all([business, ccc, pin, amount]):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        # Buscar la tarjeta de crédito en la base de datos
        try:
            credit_card = CreditCard.objects.get(card_code=ccc)
        except CreditCard.DoesNotExist:
            return JsonResponse({'error': 'Tarjeta de crédito no encontrada'}, status=400)

        # Verificar el PIN de la tarjeta de crédito
        if not check_password(pin, credit_card.pin):
            return JsonResponse({'error': 'PIN incorrecto'}, status=403)

        # Realizar el pago y actualizar el balance de la tarjeta
        credit_card.balance -= float(amount)
        credit_card.save()

        # Devolver la respuesta de éxito
        return JsonResponse({'message': 'Pago exitoso'}, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
