from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Category, Color, Product, ProductImage,
    ProductColor, Basket, BasketItem
)

BotUser = get_user_model()


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['id', 'phone', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'uz_name',"ru_name", 'parent']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductColorSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = ProductColor
        fields = ['id', 'color', 'images', 'price']


class ProductColorWritableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'product', 'color', 'images', 'price']


class ProductSerializer(serializers.ModelSerializer):
    product_colors = ProductColorSerializer(many=True, read_only=True)
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )
    main_image = serializers.ImageField()
    class Meta:
        model = Product
        fields = ['id', 'uz_name', 'ru_name', 'main_image', 'categories', 'uz_description','ru_description', 'product_colors']


class BasketItemSerializer(serializers.ModelSerializer):
    product_color = ProductColorSerializer()

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = BasketItem
        fields = ['id', 'product_color', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class BasketSerializer(serializers.ModelSerializer):
    user = BotUserSerializer(read_only=True)
    items = BasketItemSerializer(many=True, read_only=True)

    class Meta:
        model = Basket
        fields = ['id', 'user', 'created_at', 'items']
