from django.shortcuts import render,get_object_or_404
from .models import Product

def products_lists(request):
    sale_products = Product.objects.filter(is_on_sale=True).order_by('-created_at')[:6]
    return render(request, 'product_listing.html', {'products': sale_products})


def product_details(request,id):
    product = get_object_or_404(Product,id=id)
    return render(request, 'product_details.html',{
        'product': product
    })