from typing import Any
from django.db.models.query import QuerySet
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from invoices.forms import InvoiceForm, InvoiceItemFormSet, InvoiceItemFormSetHelper
from invoices.models import Invoice
from django.db import transaction

@method_decorator(never_cache, name="dispatch")
class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    context_object_name = 'invoices'
    extra_context = {'title' : "Invoices"}
    
    def get_queryset(self) -> QuerySet[Any]:
        if('active' in self.kwargs):
            if(self.kwargs.get('active') == "active"):
                invoice_active = True
            elif(self.kwargs.get('active') == "inactive"):
                invoice_active = False
            return super().get_queryset().filter(invoice_active = invoice_active)
        else:
            return super().get_queryset()
        
    def get_context_data(self, **kwargs):
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        context['active'] = self.kwargs.get('active')
        return context

@method_decorator(never_cache, name="dispatch")
class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    context_object_name = 'Invoice'
    
@method_decorator(never_cache, name="dispatch")
class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy("invoices:list")
    extra_context = {'title' : "Invoice"}
    initial = {'invoice_status' : '1'}
        
    def get_context_data(self, **kwargs):
        data = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['invoice_item'] = InvoiceItemFormSet(self.request.POST)
            data['invoice_item_formset'] = InvoiceItemFormSetHelper()
        else:
            data['invoice_item'] = InvoiceItemFormSet()
            data['invoice_item_formset'] = InvoiceItemFormSetHelper()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        invoice_item = context['invoice_item']
        if form.is_valid() and invoice_item.is_valid():
            self.object = form.save()
            invoice_item.instance = self.object
            invoice_item.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

@method_decorator(never_cache, name="dispatch")
class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy("invoices:list")
    extra_context = {'title' : "Invoice"}
    
    def get_context_data(self, **kwargs):
        data = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['invoice_item'] = InvoiceItemFormSet(self.request.POST, instance=self.object)
            data['invoice_item_formset'] = InvoiceItemFormSetHelper()
        else:
            data['invoice_item'] = InvoiceItemFormSet(instance=self.object)
            data['invoice_item_formset'] = InvoiceItemFormSetHelper()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        invoice_item = context['invoice_item']
        if form.is_valid() and invoice_item.is_valid():
            self.object = form.save()
            invoice_item.instance = self.object
            invoice_item.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

@method_decorator(never_cache, name="dispatch")
class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy("invoices:list")
    
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.invoice_status = 0
        self.object.save()
        return HttpResponseRedirect(success_url)
    
@method_decorator(never_cache, name="dispatch")
class InvoiceItemView(LoginRequiredMixin, TemplateView):
    template_name = "invoiceitem.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['row_num'] = request.GET['invoiceitem_set-TOTAL_FORMS']
        total_forms = 0
        total_forms = int(request.GET['invoiceitem_set-TOTAL_FORMS']) + 1
        context['invoiceitem_set_TOTAL_FORMS'] = str(total_forms)
        return self.render_to_response(context)