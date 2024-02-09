from django.urls import path, re_path
from address.views import AddressDropdownView

app_name = "address"

urlpatterns = [
    path('address', AddressDropdownView.as_view(), name = "address"),
]