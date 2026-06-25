from django.shortcuts import render,get_object_or_404
from .models import Product, Category

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    
    stars_range = range(1, 6) 
    
    context = {
        'product': product,
        'categories': categories,
        'stars_range': stars_range,
    }
    return render(request, 'product_detail.html', context)