from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='prouducts/')
    description = models.TextField()
    current_price = models.IntegerField()
    original_price = models.IntegerField()
    is_on_sale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.current_price:
            discount = ((self.original_price - self.current_price) / self.original_price) * 100
            return int(round(discount))
        return 0

    def __str__(self):
        return self.title