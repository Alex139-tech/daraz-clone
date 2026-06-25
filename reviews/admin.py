from django.contrib import admin
from .models import Review,ProductQuestion
from django.utils import timezone

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'product')
    search_fields = ('user_name', 'comment', 'product__title')

    
    def save_model(self, request, obj, form, change):
        # if seller_response is provided and seller_response_time is not set, set it to current time
        if obj.seller_response and not obj.seller_response_time:
            obj.seller_response_time = timezone.now()

        elif obj.seller_response and 'seller_response' in form.changed_data:
            obj.seller_response_time = timezone.now()
            
        super().save_model(request, obj, form, change)


@admin.register(ProductQuestion)
class ProductQuestionAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'question_text', 'is_answered', 'created_at')
    list_filter = ('is_answered', 'created_at', 'product')
    search_fields = ('question_text', 'answer_text', 'product__title', 'user__username')

