from django.urls import path, re_path
from clients.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, ClientDetailView

app_name = "clients"

urlpatterns = [
    path('list', ClientListView.as_view(), name = "list"),
    path('list/<str:active>', ClientListView.as_view(), name = "list"),
    path('create', ClientCreateView.as_view(), name = "create"),
    path('detail/<int:pk>', ClientDetailView.as_view(), name = "detail"),
    path('update/<int:pk>', ClientUpdateView.as_view(), name = "update"),
    path('delete/<int:pk>', ClientDeleteView.as_view(), name = "delete"),
]