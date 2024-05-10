from django.db import models
from django.forms import DecimalField
from clients.models import Client
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Max

CURRENCY_CHOICES = (('GBP', 'British Pound'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('INR', 'Indian Rupee'), ('USD', 'US Dollar'))

def next_invoice_number():
        last_invoice = Invoice.objects.all().order_by('id').last()
        last_invoice_number = 0
        if(last_invoice):
            last_invoice_number = last_invoice.invoice_number
        return str(int(last_invoice_number)+1)

class Invoice(models.Model):
    
    INVOICE_STATUSES = {'1' : "DRAFT",
                      '2' : "SENT",
                      '3' : "REVISED",
                      '4' : "PAID",
                      '5' : "DELETED",
                      '6' : "CANCELLED",}
    
    invoice_issue_date = models.DateField(_("issue date"), auto_now=False, auto_now_add=False, blank=False, null=False)
    invoice_number = models.CharField(_("invoice number"), max_length=50, unique=True, blank=False, null=False, default = next_invoice_number)
    invoice_status = models.CharField(_("status"), max_length = 150, choices = INVOICE_STATUSES)
    invoice_total = models.DecimalField(_("total"), max_digits=14, decimal_places=2, blank=False, null=False)
    invoice_date_created = models.DateTimeField(_("created date"), auto_now=False, auto_now_add=True)
    invoice_date_modified = models.DateTimeField(_("modified date"), auto_now=True, auto_now_add=False)
    client_id = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    
    @property
    def client_invoice_balance(self):
        return self.objects.filter(invoice_status__in = [2,3]).aggregate(Sum("invoice_total", default=0)).get('invoice_total__sum')
    

class InvoiceItem(models.Model):
    
    item_order = models.PositiveSmallIntegerField(_("order"), default=0, blank=True, null=True)
    item_description = models.TextField(_("description"), max_length=500, blank=False, null=False, default='')
    item_quantity = models.DecimalField(_("quantity"), max_digits=14, decimal_places=2, blank=False, null=False)
    item_price = models.DecimalField(_("unit price"), max_digits=14, decimal_places=2, blank=False, null=False)
    item_total = models.DecimalField(_("total"), max_digits=14, decimal_places=2, blank=False, null=False)
    item_date_created = models.DateTimeField(_("created date"), auto_now=False, auto_now_add=True)
    item_date_modified = models.DateTimeField(_("modified date"), auto_now=True, auto_now_add=False)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)