from django.conf import settings

# |                  | $[0€-50€)$ | $[50€-500€)$ | $≥500€$ |
# | ---------------- | ---------- | ------------ | ------- |
# | Transf. saliente | 2%         | 4%           | 6%      |
# | Transf. entrante | 1%         | 2%           | 3%      |
# | Pagos            | 3%         | 5%           | 7%      |

def calcular_comision(operation, amount):
    if operation == "salida":
        if amount <= 50:
            comision = amount * 0.02
        elif 50 < amount <= 500:
            comision = amount * 0.04
        else:
            comision = amount * 0.06
    elif operation == "entrada":
        if amount <= 50:
            comision = amount * 0.01
        elif 50 < amount <= 500:
            comision = amount * 0.02
        else:
            comision = amount * 0.03
    elif operation == "pago":
        if amount <= 50:
            comision = amount * 0.03
        elif 50 < amount <= 500:
            comision = amount * 0.05
        else:
            comision = amount * 0.07

    return comision

