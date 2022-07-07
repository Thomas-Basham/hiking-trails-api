from django.urls import path
from .views import maps, register_request,\
    login_request, logout_request, add_trail_form, documentation

urlpatterns = [
    path('', maps, name='maps'),
    path("register", register_request, name="register"),
    path("login", login_request, name="login"),
    path("logout", logout_request, name="logout"),
    path("add_trail_form", add_trail_form, name="add_trail_form"),
    path("documentation", documentation, name="documentation"),
]
