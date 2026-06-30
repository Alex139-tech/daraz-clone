from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Cart checkout
    path(
        "address/",
        views.add_address,
        name="add_address",
    ),

    # Buy now checkout
    path(
        "address/<int:product_id>/",
        views.add_address,
        name="add_address_product",
    ),
]