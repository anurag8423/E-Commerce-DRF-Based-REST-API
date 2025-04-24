from rest_framework import serializers
from .models import *
from product.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'total']
        read_only_fields = ['price', 'product', 'total']

    def get_total(self, obj):
        return obj.quantity * obj.price

    def create(self, validated_data):
        # Automatically set price from product's current price
        product = validated_data['product']
        validated_data['price'] = product.price
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # If product is changed, update price to new product's price
        if 'product' in validated_data:
            product = validated_data['product']
            validated_data['price'] = product.price
        return super().update(instance, validated_data)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 
            'user', 
            'status',
            'status_display',
            'total_price', 
            'created_at', 
            'updated_at', 
            'items'
        ]
        read_only_fields = [
            'id', 
            'user', 
            'status_display',
            'total_price', 
            'created_at', 
            'updated_at', 
            'items'
        ]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username','first_name','last_name','email','address','phone','Gender','password']
        extra_kwargs = {'password': {'write_only': True}}  # Hide password in responses

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Customer(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)  # Hash updated password
        return super().update(instance, validated_data)