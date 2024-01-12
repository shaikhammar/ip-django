from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Field
from crispy_forms.bootstrap import StrictButton
from crispy_bootstrap5.bootstrap5 import FloatingField
from users.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


USER_TYPE_CHOICES = (
    ("", "-- Select an option --"),
    (True, "Administrator"),
    (False, "Basic")
)


class UserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email', 'password1', 'password2',
                  'user_company', 'user_address_1', 
                  'user_address_2', 'user_city', 'user_state', 'user_country',
                  'user_zip', 'user_phone', 'user_fax', 'user_mobile', 'is_staff')
        widgets = {"is_staff" : forms.Select(choices=USER_TYPE_CHOICES) }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(FloatingField("first_name", wrapper_class="mb-md-0"), css_class="col-md-6"), 
                Div(FloatingField("last_name"), css_class="col-md-6"), 
                css_class="row mb-3"
                ),
            FloatingField("user_company", css_class="mb-md-0"),
            FloatingField("email", css_class="mb-md-0", autocomplete=True),
            Div(
                Div(FloatingField("password1", wrapper_class="mb-md-0"), css_class="col-md-6"), 
                Div(FloatingField("password2"), css_class="col-md-6"), 
                css_class="row mb-3"
                ),
            FloatingField("is_staff", id="user_type", css_class="mb-md-0",
                          hx_get=reverse_lazy("users:admin-info"),
                          hx_target="#admin-info",
                          hx_trigger="load, change"),
                        #   , name='user_address_2', name='user_city', name='user_state', name='user_zip', name='user_phone', name='user_fax', name='user_mobile']"),
            Div(css_id="admin-info"),
            # HTML("<hr/>"),
            # Div(
            #     Div(FloatingField("user_address_1", wrapper_class="mb-md-0"), css_class="col-md-6"), 
            #     Div(FloatingField("user_address_2"), css_class="col-md-6"), 
            #     css_class="row mb-3"
            #     ),
            # Div(
            #     Div(FloatingField("user_city", wrapper_class="mb-md-0"), css_class="col-md-5"), 
            #     Div(FloatingField("user_state"), css_class="col-md-5"),
            #     Div(FloatingField("user_zip"), css_class="col-md-2"), 
            #     css_class="row mb-3"
            #     ),
            # HTML("<hr/>"),
            # Div(
            #     Div(FloatingField("user_phone", wrapper_class="mb-md-0"), css_class="col-md-4"), 
            #     Div(FloatingField("user_fax"), css_class="col-md-4"),
            #     Div(FloatingField("user_mobile"), css_class="col-md-4"), 
            #     css_class="row mb-3"
            #     ),
            Div(Div(StrictButton('Create User', type='submit', css_class='btn-primary btn-block'), css_class='d-grid'), css_class="mt-4 mb-0"),
        )
        
class UserUpdateForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email', 'password1', 'password2',
                  'user_company', 'user_address_1', 
                  'user_address_2', 'user_city', 'user_state', 'user_country',
                  'user_zip', 'user_phone', 'user_fax', 'user_mobile', 'is_staff')
        widgets = {"is_staff" : forms.Select(choices=USER_TYPE_CHOICES) }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_city"].widget.attrs.update({"disabled" : True})
        self.fields["user_state"].widget.attrs.update({"disabled" : True})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(FloatingField("first_name", wrapper_class="mb-md-0"), css_class="col-md-6"), 
                Div(FloatingField("last_name"), css_class="col-md-6"), 
                css_class="row mb-3"
                ),
            FloatingField("user_company", css_class="mb-md-0"),
            FloatingField("email", css_class="mb-md-0", autocomplete=True),
            Div(
                Div(FloatingField("password1", wrapper_class="mb-md-0"), css_class="col-md-6"), 
                Div(FloatingField("password2"), css_class="col-md-6"), 
                css_class="row mb-3"
                ),
            FloatingField("is_staff", id="user_type", css_class="mb-md-0",
                        #   hx_get=reverse_lazy("users:admin-info"),
                        #   hx_target="#admin-info",
                        #   hx_include="[name='user_address_1'], [name='user_address_2'], [name='user_city'], [name='user_state'], [name='user_zip'], [name='user_phone'], [name='user_fax'], [name='user_mobile']",
                        #   hx_trigger="load, change"
                          ),
            Div(HTML("<hr/>"),
                Div(
                    Div(FloatingField("user_address_1", wrapper_class="mb-md-0"), css_class="col-md-6"), 
                    Div(FloatingField("user_address_2"), css_class="col-md-6"), 
                    css_class="row mb-3"
                    ),
                Div(
                    Div(FloatingField("user_city", wrapper_class="mb-md-0"), css_class="col-md-6"), 
                    Div(FloatingField("user_state"), css_class="col-md-6"),
                    css_class="row mb-3"
                    ),
                Div(
                    Div(HTML('<div id="div_id_user_city" class="form-floating mb-3 mb-md-0"> <select name="user_city" disabled="" class="select form-select" placeholder="user_city" id="id_user_city"> <option value="" selected="">---------</option></select> <label for="id_user_city">City</label> </div>'), css_class="col-md-6"), 
                    Div(HTML('<div id="div_id_user_state" class="form-floating mb-3"> <select name="user_state" disabled="" class="select form-select" placeholder="user_state" id="id_user_state"> <option value="" selected="">---------</option></select> <label for="id_user_state">State/province</label> </div>'), css_class="col-md-6"),
                    css_class="row mb-3"
                    ),
                Div(
                    Div(FloatingField("user_country", wrapper_class="mb-md-0"), css_class="col-md-6"), 
                    Div(FloatingField("user_zip"), css_class="col-md-6"), 
                    css_class="row mb-3"
                    ),
                HTML("<hr/>"),
                Div(
                    Div(FloatingField("user_phone", wrapper_class="mb-md-0"), css_class="col-md-4"), 
                    Div(FloatingField("user_fax"), css_class="col-md-4"),
                    Div(FloatingField("user_mobile"), css_class="col-md-4"), 
                    css_class="row mb-3"
                    ), 
                css_id="admin-info"
                ),
            Div(Div(StrictButton('Update User', type='submit', css_class='btn-primary btn-block'), css_class='d-grid'), css_class="mt-4 mb-0"),
        )