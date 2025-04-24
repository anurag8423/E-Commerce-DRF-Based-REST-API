from .models import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from urllib.parse import unquote



class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = filters.BooleanFilter(method='filter_in_stock')

    class Meta:
        model = Product
        fields = []

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)  
        return queryset.filter(stock=0)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        cache_key = 'product_list'
        cached_data = cache.get(cache_key)
        
        if not cached_data:
            # Optimize DB queries
            queryset = Product.objects.select_related('category')\
                                      .prefetch_related('tags')\
                                      .filter(is_active=True)
            serializer = self.get_serializer(queryset, many=True)
            cache.set(cache_key, serializer.data)
            return queryset
            
        return cached_data
    
    @method_decorator(cache_page(60*60))  
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class ProductDetail(APIView):
    def get_object(self, category_name, product_name):
        try:
            
            return Product.objects.filter(category__name__iexact=category_name).get(name__iexact=product_name)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, category_name, product_name, format=None):
        product = self.get_object(category_name, product_name)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def get_object(self):
        product_id = self.kwargs['id']
        cache_key = f'product_{product_id}_detail'
        cached_product = cache.get(cache_key)
        
        if cached_product:
            return cached_product
            
        product = Product.objects.select_related('category', 'brand')\
                                .prefetch_related('images', 'variants')\
                                .get(id=product_id)
        cache.set(cache_key, product, timeout=3600)
        return product

    
class CategoryDetail(APIView):
    def get_object(self, category_name):
        try:
            # Decode URL-encoded strings and handle case insensitivity
            decoded_name = unquote(category_name)
            return Category.objects.get(name__iexact=decoded_name)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_name, format=None):
        category = self.get_object(category_name)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
