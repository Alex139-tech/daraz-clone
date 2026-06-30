from django.contrib import admin
from .models import Order, OrderItem


# ==========================================
# ORDER ITEM INLINE
# ==========================================

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = (
        "product",
        "price",
        "quantity",
        "total_price",
    )


# ==========================================
# ORDER ADMIN
# ==========================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "payment_method",
        "items_total",
        "delivery_fee",
        "final_total",
        "is_paid",
        "created_at",
    )

    list_filter = (
        "payment_method",
        "is_paid",
        "created_at",
    )

    search_fields = (
        "id",
        "user__username",
        "user__email",
        "shipping_address__full_name",
        "shipping_address__phone_number",
    )

    readonly_fields = (
        "created_at",
        "items_total",
        "final_total",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20

    inlines = [
        OrderItemInline,
    ]

    fieldsets = (

        ("Customer Information", {

            "fields": (
                "user",
                "shipping_address",
            )

        }),

        ("Order Information", {

            "fields": (
                "payment_method",
                "order_note",
                "delivery_fee",
                "is_paid",
            )

        }),

        ("Totals", {

            "fields": (
                "items_total",
                "final_total",
            )

        }),

        ("Date", {

            "fields": (
                "created_at",
            )

        }),

    )


# ==========================================
# ORDER ITEM ADMIN
# ==========================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "product",
        "price",
        "quantity",
        "total_price",
    )

    list_filter = (
        "order__created_at",
    )

    search_fields = (
        "order__id",
        "product__title",
    )

    readonly_fields = (
        "total_price",
    )

    ordering = (
        "-id",
    )

    list_per_page = 25