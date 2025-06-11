from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class BotUserManager(BaseUserManager):
    def create_user(self, phone, name, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone number is required')
        if not name:
            raise ValueError('Name is required')

        user = self.model(phone=phone, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, name, password, **extra_fields)


# bot foydalanuvchi modeli
class BotUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = BotUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({self.phone})"


# Product-related models
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Product(models.Model):
    uz_name = models.CharField(max_length=100)
    ru_name = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='products/')
    categories = models.ManyToManyField(Category)
    description = models.TextField()

    def __str__(self):
        return self.uz_name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.image.url


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_colors')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    images = models.ManyToManyField(ProductImage)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.uz_name} - {self.color.name}"


# Basket-related models
class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='baskets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Basket #{self.id} - {self.user.phone}"


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product_color.price

    def __str__(self):
        return f"{self.quantity} x {self.product_color.product.uz_name} ({self.product_color.color.name})"
