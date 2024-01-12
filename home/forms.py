from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from crispy_forms.bootstrap import StrictButton
from crispy_bootstrap5.bootstrap5 import FloatingField
from users.models import User
from django.utils.translation import gettext_lazy as _

class LoginForm(AuthenticationForm):
    username = UsernameField(label='Email address', widget=forms.TextInput(attrs={'class':'form-control', 'type':'email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    
    def confirm_login_allowed(self, user):
        if user.is_staff and not user.is_superuser:
            raise forms.ValidationError(
                ("This account is not allowed here."),
                code='not_allowed',
            )

class SignupForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email','password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(Div(FloatingField("first_name", wrapper_class="mb-md-0"), css_class="col-md-6"), 
                Div(FloatingField("last_name"), css_class="col-md-6"), 
                css_class="row mb-3"),
            FloatingField("email", css_class="mb-md-0"),
            Div(Div(FloatingField("password1", wrapper_class="mb-md-0"), css_class="col-md-6"), 
                Div(FloatingField("password2"), css_class="col-md-6"), 
                css_class="row mb-3"),
            Div(Div(StrictButton('Create User', type='submit', css_class='btn-primary btn-block'), css_class='d-grid'), css_class="mt-4 mb-0"),
        )
