from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView
from home.forms import LoginForm, SignupForm
from users.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

@method_decorator(never_cache, name="dispatch")
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

class LogoutView(LogoutView):
    template_name = ''

class SignupView(CreateView):
    model = User
    template_name = "signup.html"
    form_class = SignupForm
    success_url = reverse_lazy('login')
