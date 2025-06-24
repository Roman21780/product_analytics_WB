from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'price': ['gte', 'lte'],
        'rating': ['gte'],
        'review_count': ['gte'],
    }