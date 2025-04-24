from django.urls import path
from .views import *

urlpatterns = [
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('place-order/', PlaceOrderAPIView.as_view(), name='place-order'),
    path('orders/<int:order_id>/update-status/', OrderStatusUpdateAPIView.as_view(), name='update-order-status'),
    path('registeration/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('profile/<int:pk>/', CustomerRetrieveUpdateDestroyView.as_view(), name='customer-detail'), 
]