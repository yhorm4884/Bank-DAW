from django.contrib import admin
from django.http import HttpResponse
import csv
import datetime

from .models import Transaction

def export_selected_as_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    
    # Campos del modelo que se incluyen en el CSV
    fields = ['agent', 'concept', 'timestamp', 'amount', 'kind']

    # Escribir la primera fila con la información del encabezado
    writer.writerow([modeladmin.model._meta.get_field(field).verbose_name for field in fields])

    # Escribir las filas de datos
    for obj in queryset:
        data_row = [getattr(obj, field) for field in fields]
        # Convertir campos de fecha a formato legible
        for i, field in enumerate(fields):
            if isinstance(getattr(obj, field), datetime.datetime):
                data_row[i] = getattr(obj, field).strftime('%d/%m/%Y')
        writer.writerow(data_row)

    return response

export_selected_as_csv.short_description = 'Export selected transactions as CSV'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('kind', 'agent', 'amount', 'timestamp')
    list_filter = ('kind', 'agent')
    search_fields = ('concept', 'amount', 'timestamp')
    actions = [export_selected_as_csv]
