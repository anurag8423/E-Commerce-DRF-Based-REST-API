from rest_framework import serializers

from .models import *

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(source='category.name')
    class Meta:
        model = Product
        fields = ('id','name','description','price','stock','get_absolute_url','category')

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
        )