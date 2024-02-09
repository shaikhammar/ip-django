from atexit import register
from django.contrib import admin
from invoices.forms import InvoiceItemFormSet

from invoices.models import Invoice, InvoiceItem

# Register your models here.
class InvoiceItemAdmin(admin.TabularInline):
    model = InvoiceItem

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemAdmin]
    


