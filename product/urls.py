from django.urls import path, include
from product.views import *
urlpatterns = [
   path('products-list/',ProductListView.as_view(),name="products-list"),
   path('products/<str:category_name>/<str:product_name>/',ProductDetail.as_view(), name='product-detail'),
   path('categories/<str:category_name>/', CategoryDetail.as_view(), name='category-detail'),
]