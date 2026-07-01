
from django.db import models
from django.db.models import Avg


class Category(models.Model):
    """
    Model representing product categories with a self-referential parent 
    field to support multi-level subcategories (e.g., Bedding & Bath > Bath > Bathroom Scales).
    """
    name = models.CharField(max_length=150)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='subcategories'
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        # Displays the full category path in Django Admin
        full_path = [self.name]
        p = self.parent
        while p is not None:
            full_path.append(p.name)
            p = p.parent
        return ' -> '.join(reversed(full_path))


class Product(models.Model):
    # Category Relationship
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='products'
    )

    # Core Product Information
    title = models.CharField(max_length=200)
    brand_name = models.CharField(max_length=100, default="No Brand", blank=True, null=True)
    image = models.ImageField(upload_to='products/')

    description = models.TextField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_on_sale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Dynamic Ratings & Q&A Fields
    # Note: rating and total_ratings are handled dynamically via @property below.
    answered_questions = models.IntegerField(default=0) 

    # Dynamic Shipping and Delivery Fields 
    delivery_charge = models.IntegerField(default=105)
    delivery_days = models.CharField(max_length=100, default="Guaranteed by 28 Jun")
    cash_on_delivery = models.BooleanField(default=True)
    
    # Customer Protection and Warranty Status Fields
    change_of_mind = models.BooleanField(default=True)   
    return_days = models.IntegerField(default=14)        
    warranty_available = models.BooleanField(default=False) 
    warranty_info = models.CharField(max_length=200, blank=True, null=True, default="Warranty not available")

    # Dynamic Seller Panel Metrics
    seller_name = models.CharField(max_length=100, default="EOrison")
    positive_seller_ratings = models.IntegerField(default=84) 
    ship_on_time = models.IntegerField(default=100)           
    chat_response_rate = models.CharField(max_length=50, default="Not enough data")

    # Item Form / Inventory Metric
    item_form = models.CharField(max_length=50, blank=True, null=True, default="Solid")

    def __str__(self):
        return self.title

    # --- Dynamic Properties ---

    @property
    def total_similar_form_items(self):
        if self.item_form:
            return Product.objects.filter(item_form=self.item_form).count()
        return 0

    @property
    def rating(self):
        # Calculates average rating dynamically from related reviews
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 1) if avg_rating else 0.0

    @property
    def total_ratings(self):
        # Counts total reviews dynamically
        return self.reviews.count()

    @property
    def answered_questions_count(self):
        return self.questions.filter(is_answered=True).count()

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.current_price:
            discount = ((self.original_price - self.current_price) / self.original_price) * 100
            return int(round(discount))
        return 0

    @property
    def star_breakdown(self):
        """
        Dynamically filters and counts reviews from the connected reviews app
        to calculate accurate percentages for Daraz-style breakdown bars.
        """
        total = self.total_ratings
        if total == 0:
            return {'five': 0, 'four': 0, 'three': 0}
        
        # Count individual star buckets
        five_star = self.reviews.filter(rating=5).count()
        four_star = self.reviews.filter(rating=4).count()
        three_star = self.reviews.filter(rating=3).count()
        
        return {
            'five': int((five_star / total) * 100),
            'four': int((four_star / total) * 100),
            'three': int((three_star / total) * 100),
        }


class Voucher(models.Model):
    """
    Model representing dynamic discount coupons/vouchers that can be 
    linked to specific products (e.g., Rs. 50 OFF, 10% OFF).
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_vouchers')
    discount_title = models.CharField(max_length=50, help_text="e.g., Rs. 50 OFF or 10% OFF")
    min_spend = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.discount_title} for {self.product.title}"
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Gallery Image for {self.product.title}"
    

# this is my inventory
class Stock(models.Model):

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="stock"
    )

    quantity = models.PositiveIntegerField(
        default=0
    )

    low_stock_alert = models.PositiveIntegerField(
        default=5
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"
    



# this is my shipping costing handling model
class ShippingSetting(models.Model):
      shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=390)
      free_shipping_min_order = models.DecimalField(max_digits=10, decimal_places=2, default=5000)
      
      def __str__(self):
        return "Shipping Settings"