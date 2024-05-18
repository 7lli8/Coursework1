from django.urls import path

from .views import (
    signup_view,
    signin_view,
    logout_view,
    account_view,
    contacts_view,
    help_view,
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("signin/", signin_view, name="signin"),
    path("logout/", logout_view, name="logout"),
    path("account/", account_view, name="account"),
    path("contacts/", contacts_view, name="contacts"),
    path("help/", help_view, name="help"),
]
