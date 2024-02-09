from django.shortcuts import render
from django.views.generic import TemplateView
from address.models import Region, City

# Create your views here.
class AddressDropdownView(TemplateView):
    template_name = "address.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if(request.GET.get('client_country')):
            country_id = request.GET.get('client_country')
            states = Region.objects.filter(country_id = country_id)
            context["states"] = states
        elif(request.GET.get('client_state')):
            state_id = request.GET.get('client_state')
            cities = City.objects.filter(region_id = state_id)
            context["cities"] = cities
        return self.render_to_response(context)