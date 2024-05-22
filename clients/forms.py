from django import forms
from clients.models import Client
from django.utils.translation import gettext_lazy as _

class ClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        fields = ['client_name', 'client_address', 'client_phone',
                  'client_fax', 'client_mobile', 'client_email', 'client_web',
                  'client_currency', 'client_active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.label == 'Active':
                pass
            else:
                field.widget.attrs['class'] = 'form-control mb-3'
                field.widget.attrs['placeholder'] = 'placeholder'
                
class InvoiceExtractionForm(forms.Form):
    client_id = forms.CharField(widget=forms.HiddenInput())
    file = forms.FileField(label='Upload PDF File:', required=True, allow_empty_file=False)