from django.db import models
from products.models import Product 
from django.contrib.auth.models import User

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100, default="Anonymous")
    rating = models.FloatField(default=5.0)
    comment = models.TextField()
    color_family = models.CharField(max_length=50, blank=True, null=True, default="Standard")
    created_at = models.DateField(auto_now_add=True)
    
    # Seller Response Fields
    seller_response = models.TextField(blank=True, null=True)
    seller_response_time = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"{self.rating} Star Review by {self.user_name}"
    
class ProductQuestion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    question_text = models.TextField()
    answer_text = models.TextField(blank=True, null=True)
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q on {self.product.title}: {self.question_text[:30]}"