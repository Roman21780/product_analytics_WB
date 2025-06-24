# products/views.py
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from products.models import Product
from products.serializers import ProductSerializer


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    min_rating = filters.NumberFilter(field_name='rating', lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['min_price', 'min_rating']

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter