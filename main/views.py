from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import (
    BotUser, Category, Color, Product, ProductImage,
    ProductColor, Basket, BasketItem
)
from .serializers import *


class BotUserViewSet(viewsets.ModelViewSet):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer
    permission_classes = [IsAdminUser]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminUser]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]


class ProductColorViewSet(viewsets.ModelViewSet):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorWritableSerializer  # write-enabled
    permission_classes = [IsAdminUser]


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [IsAdminUser]


class BasketItemViewSet(viewsets.ModelViewSet):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemSerializer
    permission_classes = [IsAdminUser]
