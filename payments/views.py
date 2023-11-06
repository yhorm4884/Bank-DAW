from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PaymentForm

def payment_form(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Procesar el formulario y redirigir a la vista de procesamiento
            return redirect('payments:process_payment')
    else:
        form = PaymentForm()
    return render(request, 'payments/payment_form.html', {'form': form})

def process_payment(request):
    if request.method == 'POST':
        # Procesar el pago aquí y devolver una respuesta adecuada
        return HttpResponse('Pago procesado con éxito')
    return HttpResponse('Error en el procesamiento del pago')
