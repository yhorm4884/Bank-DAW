from django.conf import settings
from prettyconf import config

# |                  | $[0€-50€)$ | $[50€-500€)$ | $≥500€$ |
# | ---------------- | ---------- | ------------ | ------- |
# | Transf. saliente | 2%         | 4%           | 6%      |
# | Transf. entrante | 1%         | 2%           | 3%      |
# | Pagos            | 3%         | 5%           | 7%      |

SALIDA_COMISIONES = {
    (0, 50): float(config("SALIDA_0_50", default=0.02)),
    (50, 500): float(config("SALIDA_50_500", default=0.04)),
    (500, float('inf')): float(config("SALIDA_500_INF", default=0.06)),
}

ENTRADA_COMISIONES = {
    (0, 50): float(config("ENTRADA_0_50", default=0.01)),
    (50, 500): float(config("ENTRADA_50_500", default=0.02)),
    (500, float('inf')): float(config("ENTRADA_500_INF", default=0.03)),
}

PAGO_COMISIONES = {
    (0, 50): float(config("PAGO_0_50", default=0.03)),
    (50, 500): float(config("PAGO_50_500", default=0.05)),
    (500, float('inf')): float(config("PAGO_500_INF", default=0.07)),
}

def calcular_comision(operation, amount):
    comisiones = None

    if operation == "salida":
        comisiones = SALIDA_COMISIONES
    elif operation == "entrada":
        comisiones = ENTRADA_COMISIONES
    elif operation == "pago":
        comisiones = PAGO_COMISIONES

    for (min_amount, max_amount), porcentaje in comisiones.items():
        if min_amount < amount <= max_amount:
            return amount * porcentaje

