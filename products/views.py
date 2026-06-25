from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    """
    Fetches the latest 6 products that are on sale
    and renders them on the homepage slider.
    """
    products = Product.objects.filter(
        is_on_sale=True
    ).order_by('-created_at')[:6]

    context = {
        'products': products
    }

    return render(request, 'slider.html', context)


def product_detail(request, id):
    """
    Fetches a single product by its ID, fetches all available categories 
    for the dropdown menu, and generates a sequence from 1 to 5 
    to handle dynamic star ratings in the frontend template.
    """
    product = get_object_or_404(Product, id=id)
    
    # Fetches all categories to display in the main navigation sidebar/dropdown
    categories = Category.objects.all()
    
    # Generates a sequence from 1 to 5 for the template star loop
    stars_range = range(1, 6)

    context = {
        'product': product,
        'categories': categories,  # Added categories to context
        'stars_range': stars_range,
    }

    return render(request, 'product_details.html', context)


# NEW: Product Listing View to display all your admin dashboard products
def product_list(request):
    """
    Fetches all products from the database, ordered by latest additions,
    and renders them on the product listing archive page grid.
    """
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'product_list.html', {'products': products})