from django.urls import path
from .views import ConvertTokenView, ContactListCreateView, ContactDetailView

app_name = "contact_manager_app"

urlpatterns = [
    path("auth/login/", ConvertTokenView.as_view(), name="login"),
    path("contacts/", ContactListCreateView.as_view(), name="contact-list-create"),
    path("contacts/<int:id>/", ContactDetailView.as_view(), name="contact-detail"),
]
