from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from products.models import Product
from accounts.models import Address
from carts.models import Cart
from django.contrib import messages
from .models import OrderItem,Order

@login_required
def checkout(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    shipping_address = Address.objects.filter(
        user=request.user
    ).first()

    subtotal = product.current_price
    shipping = Decimal("390.00")
    discount = Decimal("0.00")
    total = subtotal + shipping - discount

    context = {
        "product": product,
        "shipping_address": shipping_address,
        "subtotal": subtotal,
        "shipping": shipping,
        "discount": discount,
        "total": total,
    }

    return render(request, "order/checkout.html", context)


# this is my cart 
@login_required
def cart_checkout(request):

    # Get cart
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cart.cart_items.all()

    # Cart Empty
    if not cart_items.exists():

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("cart_view")

    # Shipping Address
    shipping_address = Address.objects.filter(
        user=request.user
    ).first()

    # Calculate Total
    subtotal = Decimal("0.00")

    for item in cart_items:
        subtotal += item.total_price

    shipping = Decimal("390.00")
    discount = Decimal("0.00")
    total = subtotal + shipping - discount

    # ==========================
    # PLACE ORDER
    # ==========================
    if request.method == "POST":

        if not shipping_address:

            messages.error(
                request,
                "Please add your delivery address first."
            )

            return redirect("add_address")

        payment_method = request.POST.get(
            "payment_method",
            "COD"
        )

        order_note = request.POST.get(
            "order_note",
            ""
        )

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

        # Empty Cart
        cart_items.delete()

        messages.success(
            request,
            "Order placed successfully."
        )

        return redirect("home")
    

    # ==========================
    # PAGE LOAD
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

    return render(

        request,

        "order/cart_checkout.html",

        context,

    )


# single product create function
@login_required
def checkout(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    shipping_address = Address.objects.filter(user=request.user).first()

    subtotal = product.current_price
    shipping = Decimal("390.00")
    discount = Decimal("0.00")
    total = subtotal + shipping - discount

    # ==========================
    # PLACE ORDER
    # ==========================
    if request.method == "POST":

        if not shipping_address:

            messages.error(
                request,
                "Please add your delivery address first."
            )

            return redirect(
                "add_address_product",
                product_id=product.id
            )

        payment_method = request.POST.get(
            "payment_method",
            "COD"
        )

        order_note = request.POST.get(
            "order_note",
            ""
        )

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


        )

        messages.success(
            request,
            "Order placed successfully."
        )

        return redirect("home")

    context = {

        "product": product,

        "shipping_address": shipping_address,

        "subtotal": subtotal,

        "shipping": shipping,

        "discount": discount,

        "total": total,

    }

    return render(
        request,
        "order/checkout.html",
        context
    )