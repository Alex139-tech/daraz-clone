from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=15, blank=True)

    wishlist = models.ManyToManyField(
        "products.Product",
        blank=True,
        related_name="wishlisted_by"
    )

    def __str__(self):
        return self.user.username

class Address(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)

    phone_number = models.CharField(max_length=10)

    address = models.TextField()

    city = models.CharField(max_length=100)

    province = models.CharField(max_length=100)

    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name