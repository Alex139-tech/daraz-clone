from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = (
        'title', 
        'current_price', 
        'original_price', 
        'get_discount_percentage',
        'is_on_sale', 
        'created_at'
    )
    
    list_filter = ('is_on_sale', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('current_price', 'original_price', 'is_on_sale')
    date_hierarchy = 'created_at'

    
    @admin.display(description='Discount (%)')
    def get_discount_percentage(self, obj):
        return f"{obj.discount_percentage}%" if obj.discount_percentage > 0 else "0%"