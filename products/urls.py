from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home'),
   path('products/', views.product_list, name='product_list'), # New Listing Route
   path('product/<int:id>/', views.product_detail, name='product_detail'),
   path('wishlist/<int:product_id>/',views.toggle_wishlist,name="toggle_wishlist"),
]

