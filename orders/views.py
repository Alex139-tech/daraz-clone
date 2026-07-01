from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product, ShippingSetting, Stock
from accounts.models import Address
from carts.models import Cart
from .models import OrderItem, Order


def get_shipping_charge():
    shipping_setting = ShippingSetting.objects.order_by("-id").first()
    return shipping_setting.shipping_charge if shipping_setting else Decimal("390.00")


@login_required
def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    shipping_address = Address.objects.filter(user=request.user).first()

    subtotal = product.current_price
    shipping = get_shipping_charge()
    discount = Decimal("0.00")
    total = subtotal + shipping - discount

    # ==========================
    # PLACE ORDER (POST)
    # ==========================
    if request.method == "POST":
        if not shipping_address:
            messages.error(request, "Please add your delivery address first.")
            return redirect("add_address_product", product_id=product.id)

        payment_method = request.POST.get("payment_method", "COD")
        order_note = request.POST.get("order_note", "")

        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            payment_method=payment_method,
            order_note=order_note,
            delivery_fee=shipping,
            is_paid=False,
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            price=product.current_price,
            quantity=1,
        )

        messages.success(request, "Order placed successfully.")
        return redirect("home")

    # ==========================
    # PAGE LOAD (GET)
    # ==========================
    context = {
        "product": product,
        "shipping_address": shipping_address,
        "subtotal": subtotal,
        "shipping": shipping,
        "discount": discount,
        "total": total,
    }
    return render(request, "order/checkout.html", context)


@login_required
def cart_checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart_view")

    shipping_address = Address.objects.filter(user=request.user).first()

    subtotal = sum(item.total_price for item in cart_items)
    shipping = get_shipping_charge()
    discount = Decimal("0.00")
    total = subtotal + shipping - discount

    # ==========================
    # PLACE ORDER (POST)
    # ==========================
    if request.method == "POST":
        if not shipping_address:
            messages.error(request, "Please add your delivery address first.")
            return redirect("add_address")

        payment_method = request.POST.get("payment_method", "COD")
        order_note = request.POST.get("order_note", "")

        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            payment_method=payment_method,
            order_note=order_note,
            delivery_fee=shipping,
            is_paid=False,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.current_price,
                quantity=item.quantity,
            )

        cart_items.delete()

        messages.success(request, "Order placed successfully.")
        return redirect("home")

    # ==========================
    # PAGE LOAD (GET)
    # ==========================
    context = {
        "cart": cart,
        "cart_items": cart_items,
        "shipping_address": shipping_address,
        "subtotal": subtotal,
        "shipping": shipping,
        "discount": discount,
        "total": total,
    }
    return render(request, "order/cart_checkout.html", context)