from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    """
    One shopping cart per user.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.user.username}'s Cart"

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.cart_items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.cart_items.all())

    @property
    def total_saving(self):
        return sum(item.total_discount for item in self.cart_items.all())


class CartItem(models.Model):
    """
    Stores a snapshot of the product price when it was added to the cart.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(default=1)

    current_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_cart_product"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.quantity} × {self.product.title}"

    @property
    def total_price(self):
        return self.current_price * self.quantity

    @property
    def total_original_price(self):
        return self.original_price * self.quantity

    @property
    def total_discount(self):
        return (
            self.total_original_price -
            self.total_price
        )


class Voucher(models.Model):
    """
    Voucher/Coupon model.
    """

    DISCOUNT_TYPE = (
        ("fixed", "Fixed Amount"),
        ("percent", "Percentage"),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="vouchers"
    )

    voucher_code = models.CharField(
        max_length=30,
        unique=True
    )

    discount_title = models.CharField(
        max_length=100
    )

    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE,
        default="fixed"
    )

    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    min_spend = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["voucher_code"]

    def __str__(self):
        return f"{self.voucher_code} ({self.discount_title})"
    

@property
def total_price(self):
    return self.current_price * self.quantity