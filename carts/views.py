from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Cart, CartItem
from products.models import Product


# ==========================================
# CART PAGE
# ==========================================

@login_required
def cart_view(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cart.cart_items.select_related("product")

    context = {
        "cart": cart,
        "cart_items": cart_items,
    }

    return render(
        request,
        "carts/carts.html",
        context
    )


# ==========================================
# ADD TO CART
# ==========================================

@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            "current_price": product.current_price,
            "original_price": product.original_price,
            "quantity": 1,
        }
    )

    if not created:

        cart_item.quantity += 1
        cart_item.save(update_fields=["quantity"])

    messages.success(
        request,
        "Product added to cart successfully."
    )

    return redirect(
        request.META.get("HTTP_REFERER", "cart_view")
    )


# ==========================================
# REMOVE ITEM
# ==========================================

@login_required
def remove_from_cart(request, product_id):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_item = get_object_or_404(
        CartItem,
        cart=cart,
        product_id=product_id
    )

    cart_item.delete()

    messages.success(
        request,
        "Product removed from cart."
    )

    return redirect("cart_view")



@login_required
def increase_quantity(request, product_id):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_item = get_object_or_404(
        CartItem,
        cart=cart,
        product_id=product_id
    )

    cart_item.quantity += 1

    cart_item.save(update_fields=["quantity"])

    return redirect("cart_view")


# ==========================================
# DECREASE
# ==========================================

@login_required
def decrease_quantity(request, product_id):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_item = get_object_or_404(
        CartItem,
        cart=cart,
        product_id=product_id
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save(update_fields=["quantity"])

    else:

        messages.warning(
            request,
            "Minimum quantity is 1."
        )

    return redirect("cart_view")