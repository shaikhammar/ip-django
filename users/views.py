from typing import Any
from django.views.generic import ListView, CreateView, TemplateView, DeleteView, UpdateView
from users.models import User
from users.forms import UserForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
import logging

# Create your views here.

@method_decorator(never_cache, name="dispatch")
class UserList(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "users"
    extra_context = {'title' : "Users"}

@method_decorator(never_cache, name="dispatch")
class UserCreate(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("users:list")
    extra_context = {'title' : 'User'}

@method_decorator(never_cache, name="dispatch")
class AdminInfoView(LoginRequiredMixin, TemplateView):
    template_name = "admin_info.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print(request)
        context['user_address_1'] = request.GET.get('user_address_1')
        context['user_address_2'] = request.GET.get('user_address_2')
        context['user_city'] = request.GET.get('user_city')
        context['user_state'] = request.GET.get('user_state')
        context['user_zip'] = request.GET.get('user_zip')
        context['user_phone'] = request.GET.get('user_phone')
        context['user_fax'] = request.GET.get('user_fax')
        context['user_mobile'] = request.GET.get('user_mobile')
        context['is_staff'] = request.GET.get('is_staff')
        return self.render_to_response(context)
    
@method_decorator(never_cache, name="dispatch")
class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users:list")

@method_decorator(never_cache, name="dispatch")
class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("users:list")
    extra_context = {'title' : 'User'}