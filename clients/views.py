from datetime import datetime, timezone
import os
import re
from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from clients.forms import ClientForm, InvoiceExtractionForm
from clients.models import Client
from invoices.models import Invoice, InvoiceItem
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from ip import settings  # PyMuPDF
import fitz


@method_decorator(never_cache, name="dispatch")
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    context_object_name = 'clients'
    extra_context = {'title' : "Clients"}
    
    def get_queryset(self) -> QuerySet[Any]:
        if('active' in self.kwargs):
            if(self.kwargs.get('active') == "active"):
                client_active = True
            elif(self.kwargs.get('active') == "inactive"):
                client_active = False
            return super().get_queryset().filter(client_active = client_active)
        else:
            return super().get_queryset()
        
    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context['active'] = self.kwargs.get('active')
        return context

@method_decorator(never_cache, name="dispatch")
class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    context_object_name = 'client'
    
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        # print(Invoice.objects.filter(client_id = self.object.pk))
        context['invoices'] = Invoice.objects.filter(client_id = self.object.pk)
        context['client_invoice_total'] = Invoice.objects.filter(invoice_status__in = [2,3]).aggregate(Sum("invoice_total", default=0)).get('invoice_total__sum')
        context['client_invoice_paid'] = context['client_invoice_total']
        context['client_invoice_balance'] = context['client_invoice_total'] - context['client_invoice_paid']
        return context
        
@method_decorator(never_cache, name="dispatch")
class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("clients:list")
    extra_context = {'title' : "Client"}

@method_decorator(never_cache, name="dispatch")
class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("clients:list")
    extra_context = {'title' : "Client"}

@method_decorator(never_cache, name="dispatch")
class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("clients:list")
    
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.client_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)
    
@method_decorator(never_cache, name="dispatch")
class ClientAddressView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "client_address.html"
    
    def get_object(self, request, queryset=None):
        """
        Return the object the view is displaying.
        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk=self.kwargs.get(self.pk_url_kwarg)
        if(request.GET.get('client_id')):
            pk = request.GET.get('client_id')
        else:
            pk = 5
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(request)
        context = self.get_context_data(object=self.object)
        context['client_address'] = self.object.client_address
        context['client_currency'] = self.object.client_currency
        return self.render_to_response(context)

@method_decorator(never_cache, name="dispatch")
class PDFDataExtractorView(LoginRequiredMixin, FormView):
    form_class = InvoiceExtractionForm
    template_name = 'invoice_extractor_form.html'
    
    def form_valid(self, form):
        uploaded_file = form.cleaned_data['file']
        client_id = form.cleaned_data['client_id']
        temp_file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        with open(temp_file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        # Assuming 'pdf_file' contains the path to the uploaded PDF file
        extracted_data = self.extract_invoice_details(temp_file_path)
        self.save_extracted_data(extracted_data, client_id)
        os.remove(temp_file_path)
        # extracted_data = "Test Data"
        return JsonResponse({'success': True, 'data': extracted_data})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})
    
    def extract_invoice_details(self, pdf_path):
        document = fitz.open(pdf_path)
        text = ''
        for page in document:
            text += page.get_text()

        # Extracting details from the text
        invoice_number = self.extract_between(text, 'Invoice Number:', 'Internal Invoice Reference:')
        internal_invoice_number = self.extract_between(text, 'Internal Invoice Reference:', 'Invoice Date:')
        invoice_date = self.extract_between(text, 'Invoice Date:', 'From:')
        gross_total = self.extract_between(text, 'Net Total', 'Gross Total')
        
        

        return {
            'invoice_number': invoice_number.strip() if invoice_number else 'N/A',
            'internal_invoice_number': internal_invoice_number.strip() if internal_invoice_number else 'N/A',
            'invoice_date': invoice_date.strip() if invoice_date else 'N/A',
            'gross_total': gross_total.strip() if gross_total else 'N/A',
        }

    def extract_between(self, text, start, end):
        try:
            return text.split(start)[1].split(end)[0]
        except IndexError:
            return None
        
    def save_extracted_data(self, data, client_id):
        client = Client.objects.get(pk=client_id) 
        
        # Parse and format the invoice date
        try:
            invoice_date = datetime.strptime(data['invoice_date'].strip(), '%d/%m/%Y').date()
        except ValueError:
            invoice_date = None
            
         # Extract the number from the gross total string
        gross_total = self.extract_number(data['gross_total'])

        invoice = Invoice.objects.create(
            invoice_issue_date=invoice_date if invoice_date != 'N/A' else timezone.now().date(),
            invoice_number=data['invoice_number'],
            invoice_status='2',  # Default to 'SENT'
            invoice_total=gross_total,
            client_id=client,
        )
        
        items_data = [
            {
                'description': data['internal_invoice_number'],
                'quantity': 1,
                'price': gross_total,
                'total': gross_total,
            }
        ]

        for item_data in items_data:
            InvoiceItem.objects.create(
                item_description=item_data['description'],
                item_quantity=item_data['quantity'],
                item_price=item_data['price'],
                item_total=item_data['total'],
                invoice_id=invoice,
            )
            
    def extract_number(self, currency_string):
        # Define a regular expression pattern to match the number
        pattern = r'\b\d+\.\d{2}\b'
        match = re.search(pattern, currency_string)
        if match:
            return match.group()
        return None