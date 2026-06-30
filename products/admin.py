from django.contrib import admin
from .models import Product, Category, Voucher, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product Categories.
    """
    list_display = ('name', 'parent')
    search_fields = ('name',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4 


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Products with organized fieldsets for easier data entry.
    """
    inlines = [ProductImageInline]

    # Columns to display in the admin list view
    list_display = (
        'title', 
        'category',
        'current_price', 
        'original_price', 
        'stock',
        'get_discount_percentage',
        'is_on_sale', 
        'created_at'
    )
    
    list_filter = ('category', 'is_on_sale', 'created_at')
    search_fields = ('title', 'description', 'seller_name')
    list_editable = ('category', 'current_price', 'original_price', 'is_on_sale')
    date_hierarchy = 'created_at'

    # Groups fields into separate sections when creating/editing a product
    fieldsets = (
        ('Core Information', {
            'fields': (
                'title', 'category', 'brand_name', 'image', 'description', 
                'current_price', 'original_price', 'is_on_sale'
            )
        }),
        ('Shipping & Delivery', {
            'fields': ('delivery_charge', 'delivery_days', 'cash_on_delivery')
        }),
        ('Warranty & Returns', {
            'fields': ('change_of_mind', 'return_days', 'warranty_available', 'warranty_info')
        }),
        ('Seller Dashboard Metrics', {
            'fields': ('seller_name', 'positive_seller_ratings', 'ship_on_time', 'chat_response_rate')
        }),
    )

    @admin.display(description='Discount (%)')
    def get_discount_percentage(self, obj):
        return f"{obj.discount_percentage}%" if obj.discount_percentage > 0 else "0%"
    

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product Vouchers.
    """
    list_display = ('discount_title', 'product', 'min_spend', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('discount_title', 'product__title')