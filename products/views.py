from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    products = Product.objects.filter(
        is_on_sale=True
    ).order_by('-created_at')[:6]

    context = {
        'products': products
    }

    return render(request, 'slider.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, 'product_details.html', {
        'product': product
    })