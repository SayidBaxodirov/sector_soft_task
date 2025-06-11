from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('users', BotUserViewSet)
router.register('categories', CategoryViewSet)
router.register('colors', ColorViewSet)
router.register('products', ProductViewSet)
router.register('product-images', ProductImageViewSet)
router.register('product-colors', ProductColorViewSet)
router.register('baskets', BasketViewSet)
router.register('basket-items', BasketItemViewSet)

urlpatterns = router.urls
