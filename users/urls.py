from django.urls import path, re_path
from users.views import UserList, UserCreate, AdminInfoView, UserDelete, UserUpdate

app_name = "users"

urlpatterns = [
    path('', UserList.as_view(), name = "list"),
    path('create', UserCreate.as_view(), name = "create"),
    path('admin_info', AdminInfoView.as_view(), name = "admin-info"),
    path('update/<int:pk>', UserUpdate.as_view(), name = "update"),
    path('delete/<int:pk>', UserDelete.as_view(), name = "delete"),
]