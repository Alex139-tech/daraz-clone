from django.db import models
from django.contrib.auth.models import User

from products.models import Product
from accounts.models import Address


class Order(models.Model):

    PAYMENT_CHOICES = [
        ("COD", "Cash On Delivery"),
        ("ESEWA", "eSewa"),
        ("KHALTI", "Khalti"),
        ("IME", "IME Pay"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="COD"
    )

    order_note = models.TextField(
        blank=True,
        null=True
    )

    delivery_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=390.00
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_paid = models.BooleanField(
        default=False
    )

    @property
    def items_total(self):
        return sum(
            item.total_price
            for item in self.order_items.all()
        )

    @property
    def final_total(self):
        return self.items_total + self.delivery_fee

    def __str__(self):
        return f"Order #{self.id}"
    
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"