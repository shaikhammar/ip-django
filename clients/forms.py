from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Field
from crispy_forms.bootstrap import StrictButton
from crispy_bootstrap5.bootstrap5 import FloatingField
from clients.models import Client
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_name', 'client_address_1', 'client_address_2', 'client_city',
                  'client_state', 'client_country', 'client_zip', 'client_phone',
                  'client_fax', 'client_mobile', 'client_email', 'client_web',
                  'client_currency', 'client_active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            print(field.label)
            if field.label == 'Active':
                pass
            else:
                field.widget.attrs['class'] = 'form-control mb-3'
                field.widget.attrs['placeholder'] = 'placeholder'
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         # Div(
    #         #     Div(FloatingField("first_name", wrapper_class="mb-md-0"), css_class="col-md-6"), 
    #         #     Div(FloatingField("last_name"), css_class="col-md-6"), 
    #         #     css_class="row mb-3"
    #         #     ),
    #         FloatingField("client_name", css_class="mb-md-0"),
    #         # FloatingField("email", css_class="mb-md-0", autocomplete=True),
    #         # Div(
    #         #     Div(FloatingField("password1", wrapper_class="mb-md-0"), css_class="col-md-6"), 
    #         #     Div(FloatingField("password2"), css_class="col-md-6"), 
    #         #     css_class="row mb-3"
    #         #     ),
    #         FloatingField("is_staff", id="user_type", css_class="mb-md-0",
    #                     #   hx_get=reverse_lazy("users:admin-info"),
    #                     #   hx_target="#admin-info",
    #                     #   hx_include="[name='user_address_1'], [name='user_address_2'], [name='user_city'], [name='user_state'], [name='user_zip'], [name='user_phone'], [name='user_fax'], [name='user_mobile']",
    #                     #   hx_trigger="load, change"
    #                       ),
    #         Div(HTML("<hr/>"),
    #             Div(
    #                 Div(FloatingField("user_address_1", wrapper_class="mb-md-0"), css_class="col-md-6"), 
    #                 Div(FloatingField("user_address_2"), css_class="col-md-6"), 
    #                 css_class="row mb-3"
    #                 ),
    #             Div(
    #                 Div(FloatingField("user_city", wrapper_class="mb-md-0"), css_class="col-md-6"), 
    #                 Div(FloatingField("user_state"), css_class="col-md-6"),
    #                 css_class="row mb-3"
    #                 ),
    #             Div(
    #                 Div(HTML('<div id="div_id_user_city" class="form-floating mb-3 mb-md-0"> <select name="user_city" disabled="" class="select form-select" placeholder="user_city" id="id_user_city"> <option value="" selected="">---------</option></select> <label for="id_user_city">City</label> </div>'), css_class="col-md-6"), 
    #                 Div(HTML('<div id="div_id_user_state" class="form-floating mb-3"> <select name="user_state" disabled="" class="select form-select" placeholder="user_state" id="id_user_state"> <option value="" selected="">---------</option></select> <label for="id_user_state">State/province</label> </div>'), css_class="col-md-6"),
    #                 css_class="row mb-3"
    #                 ),
    #             Div(
    #                 Div(FloatingField("user_country", wrapper_class="mb-md-0"), css_class="col-md-6"), 
    #                 Div(FloatingField("user_zip"), css_class="col-md-6"), 
    #                 css_class="row mb-3"
    #                 ),
    #             HTML("<hr/>"),
    #             Div(
    #                 Div(FloatingField("user_phone", wrapper_class="mb-md-0"), css_class="col-md-4"), 
    #                 Div(FloatingField("user_fax"), css_class="col-md-4"),
    #                 Div(FloatingField("user_mobile"), css_class="col-md-4"), 
    #                 css_class="row mb-3"
    #                 ), 
    #             css_id="admin-info"
    #             ),
    #         Div(Div(StrictButton('Update User', type='submit', css_class='btn-primary btn-block'), css_class='d-grid'), css_class="mt-4 mb-0"),
    #     )