from django.urls import path, re_path
from invoices.views import InvoiceItemView, InvoiceListView, InvoiceCreateView, InvoiceUpdateView, InvoiceDeleteView, InvoiceDetailView

app_name = "invoices"

urlpatterns = [
    path('list', InvoiceListView.as_view(), name = "list"),
    path('list/<str:active>', InvoiceListView.as_view(), name = "list"),
    path('create', InvoiceCreateView.as_view(), name = "create"),
    path('detail/<int:pk>', InvoiceDetailView.as_view(), name = "detail"),
    path('update/<int:pk>', InvoiceUpdateView.as_view(), name = "update"),
    path('delete/<int:pk>', InvoiceDeleteView.as_view(), name = "delete"),
    path('newitem', InvoiceItemView.as_view(), name="newitem"),
]