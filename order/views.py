from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Order, OrderItem
from product.models import Product
from .serializers import *
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        order, _ = Order.objects.get_or_create(user=request.user, status='pending')
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        order, _ = Order.objects.get_or_create(user=request.user, status='pending')
        
        # Update or create order item
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'price': product.price, 'quantity': quantity}
        )
        
        if not created:
            order_item.quantity += quantity
            order_item.save()
        
        order.update_total()
        
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class PlaceOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        order = Order.objects.filter(user=request.user, status='pending').first()
        if not order:
            return Response({'error': 'No pending order found'}, status=status.HTTP_400_BAD_REQUEST)
        
        if order.items.count() == 0:
            return Response({'error': 'Cannot place empty order'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'confirmed'  # Order is now placed
        order.save()
        return Response(OrderSerializer(order).data)

class OrderStatusUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES).keys():
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer 

# Retrieve (GET), Update (PUT/PATCH), or Delete (DELETE) a customer
class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user,
            status__in=['confirmed', 'completed', 'shipped']  # Add other final statuses you use
        ).select_related('user')\
        .prefetch_related('items__product')\
        .order_by('-created_at')

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user,
            status__in=['confirmed', 'completed', 'shipped']  # Exclude pending carts
        )

