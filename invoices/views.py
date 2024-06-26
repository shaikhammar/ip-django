from typing import Any
from django import forms
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from invoices.forms import InvoiceForm, InvoiceItemForm, InvoiceItemFormSet, InvoiceItemFormSetHelper, InvoiceItemInlineFormset
from invoices.models import Invoice, InvoiceItem
from django.contrib.messages.views import SuccessMessageMixin
from xhtml2pdf import pisa
from django.template.loader import get_template

@method_decorator(never_cache, name="dispatch")
class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    context_object_name = 'invoices'
    extra_context = {'title' : "Invoices"}
    
    def get_queryset(self) -> QuerySet[Any]:
        if('status' in self.kwargs):
            return super().get_queryset().filter(invoice_status = self.kwargs.get('status'))
        else:
            return super().get_queryset()
        
    def get_context_data(self, **kwargs):
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        context['status'] = self.kwargs.get('status')
        return context

@method_decorator(never_cache, name="dispatch")
class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    context_object_name = 'invoice'
    extra_context = {'title' : "Invoice"}
    
    def get_context_data(self, **kwargs):
        data = super(InvoiceDetailView, self).get_context_data(**kwargs)
        data['invoiceitems'] = InvoiceItem.objects.filter(invoice_id = self.object.id)
        return data
    
# @method_decorator(never_cache, name="dispatch")
# class InvoiceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Invoice
#     form_class = InvoiceForm
#     success_url = reverse_lazy("invoices:list")
#     extra_context = {'title' : "Invoice"}
#     initial = {'invoice_status' : '1', 'invoice_total' : '0.00'}
#     success_message = "Invoice %(invoice_number)s was created successfully"
        
#     def get_context_data(self, **kwargs):
#         data = super(InvoiceCreateView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['invoice_item'] = InvoiceItemFormSet(self.request.POST)
#             data['invoice_item_formset'] = InvoiceItemFormSetHelper()
#         else:
#             data['invoice_item'] = InvoiceItemFormSet()
#             data['invoice_item_formset'] = InvoiceItemFormSetHelper()
#         return data

#     def form_valid(self, form):
#         context = self.get_context_data()
#         invoice_item = context['invoice_item']
#         if form.is_valid() and invoice_item.is_valid():
#             self.object = form.save()
#             invoice_item.instance = self.object
#             invoice_item.save()
#             return super().form_valid(form)
#         else:
#             return self.form_invalid(form)
    
@method_decorator(never_cache, name="dispatch")
class InvoiceUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy("invoices:list")
    extra_context = {'title' : "Invoice"}
    success_message = "Invoice %(invoice_number)s was updated successfully"
    
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
        self.object.invoice_status = 3
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
        self.object.invoice_status = 5
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
    
@method_decorator(never_cache, name="dispatch")
class InvoiceDetailPDFView(LoginRequiredMixin, DetailView):
    model = Invoice
    context_object_name = 'invoice'
    extra_context = {'title' : "Invoice"}
    template_name = 'invoices/invoice_detail_pdf.html'
    
    def get_context_data(self, **kwargs):
        data = super(InvoiceDetailPDFView, self).get_context_data(**kwargs)
        data['invoiceitems'] = InvoiceItem.objects.filter(invoice_id = self.object.id)
        return data
    
    def render_to_response(self, context, **response_kwargs):
        template = get_template(self.template_name)
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        # Construct the file name with the invoice date
        invoice_date = self.object.invoice_date_created.strftime('%m-%d-%Y')
        invoice_number = self.object.invoice_number
        file_name = f"Invoice{invoice_number}({invoice_date}).pdf"
        response['Content-Disposition'] = f'filename="{file_name}"'

        # Create PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF')

        return response
    

@method_decorator(never_cache, name="dispatch")
class InvoiceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy("invoices:list")
    extra_context = {'title' : "Invoice"}
    initial = {'invoice_status' : '1', 'invoice_total' : '0.00'}
    success_message = "Invoice %(invoice_number)s was created successfully"
    
    def clone_formset(self):
        cloned_forms = []
        if self.clone_id:
            existing_invoice = get_object_or_404(Invoice, pk=self.clone_id)
            for item in existing_invoice.invoiceitem_set.all():
                form = InvoiceItemFormSet().form(instance=item)
                cloned_forms.append(form)
        return cloned_forms

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            self.clone_id = kwargs.get('pk')  # Get the ID to clone, if provided
        else:
            self.clone_id = None
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial_data = super(InvoiceCreateView, self).get_initial()
        if self.clone_id:
            # If an invoice number is provided, retrieve the existing invoice
            existing_invoice = get_object_or_404(Invoice, pk=self.clone_id)
            # Populate initial data with the existing invoice's data
            initial_data['client_id'] = existing_invoice.client_id
            initial_data['invoice_issue_date'] = existing_invoice.invoice_issue_date
            # Populate other fields as needed
        return initial_data

    def get_context_data(self, **kwargs):
        data = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['invoice_item'] = InvoiceItemFormSet(self.request.POST)
            data['invoice_item_formset'] = InvoiceItemFormSetHelper()
        else:
            if self.clone_id:
                # If an invoice number is provided, retrieve the existing invoice
                cloned_forms = self.clone_formset()
                initial_forms = []
                for form in cloned_forms:
                    form.initial['id'] = ''
                    form.initial['invoice_id'] = ''
                    initial_forms.append(form.initial)
                form_count = len(initial_forms) + 2 #Adding 2 extra rows
                CloneInvoiceItemFormSet = forms.models.inlineformset_factory(Invoice, InvoiceItem, form=InvoiceItemForm, formset=InvoiceItemInlineFormset, extra=form_count, can_delete=True, can_delete_extra=True)
                data['invoice_item'] = CloneInvoiceItemFormSet(initial=initial_forms)
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
            print("Form or formset is invalid:", form.errors, invoice_item.errors)
            return self.form_invalid(form)
