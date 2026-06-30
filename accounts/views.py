from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .models import Address


# ==========================
# REGISTER
# ==========================
def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "user/register.html", {
        "form": form,
    })


# ==========================
# LOGIN
# ==========================
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "user/login.html")


# ==========================
# LOGOUT
# ==========================
def logout_view(request):

    logout(request)
    return redirect("login")


# ==========================
# ADD / UPDATE ADDRESS
# ==========================
@login_required
def add_address(request, product_id=None):

    address = Address.objects.filter(
        user=request.user
    ).first()

    if request.method == "POST":

        if address:

            address.full_name = request.POST.get("full_name")
            address.phone_number = request.POST.get("phone_number")
            address.address = request.POST.get("address")
            address.city = request.POST.get("city")
            address.province = request.POST.get("province")
            address.postal_code = request.POST.get("postal_code")

            address.save()

        else:

            Address.objects.create(

                user=request.user,
                full_name=request.POST.get("full_name"),
                phone_number=request.POST.get("phone_number"),
                address=request.POST.get("address"),
                city=request.POST.get("city"),
                province=request.POST.get("province"),
                postal_code=request.POST.get("postal_code"),

            )

        # Buy Now
        if product_id is not None:
            return redirect("checkout", product_id=product_id)

        # Cart Checkout
        return redirect("cart_checkout")

    return render(
        request,
        "user/add_address.html",
        {
            "address": address,
        },
    )