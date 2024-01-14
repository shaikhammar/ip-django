from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from clients.forms import ClientForm

from clients.models import Client

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