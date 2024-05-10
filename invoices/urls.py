from django.urls import path, re_path
from invoices.views import InvoiceItemView, InvoiceListView, InvoiceCreateView, InvoiceDetailPDFView, InvoiceUpdateView, InvoiceDeleteView, InvoiceDetailView

app_name = "invoices"

urlpatterns = [
    path('list', InvoiceListView.as_view(), name = "list"),
    path('list/<str:status>', InvoiceListView.as_view(), name = "list"),
    path('create', InvoiceCreateView.as_view(), name = "create"),
    path('create/<int:pk>', InvoiceCreateView.as_view(), name = "clone"),
    path('detail/<int:pk>', InvoiceDetailView.as_view(), name = "detail"),
    path('detail/<int:pk>/pdf', InvoiceDetailPDFView.as_view(), name = "detailpdf"),
    path('update/<int:pk>', InvoiceUpdateView.as_view(), name = "update"),
    path('delete/<int:pk>', InvoiceDeleteView.as_view(), name = "delete"),
    path('newitem', InvoiceItemView.as_view(), name="newitem"),
]