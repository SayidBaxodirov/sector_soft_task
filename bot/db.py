from django.contrib.auth import get_user_model

from main.models import BotUser, Category, Product, ProductColor, ProductImage, Basket, BasketItem
from asgiref.sync import sync_to_async


# user part
@sync_to_async
def get_user_by_chat_id(chat_id):
    return BotUser.objects.filter(chat_id=chat_id).first()


@sync_to_async
def create_or_update_user(chat_id, full_name, phone, language):
    return BotUser.objects.update_or_create(
        chat_id=chat_id,
        defaults={"name": full_name, "phone": phone, "language": language}
    )


@sync_to_async
def update_user_language(chat_id, new_lang):
    user = BotUser.objects.filter(chat_id=chat_id).first()
    if user:
        user.language = new_lang
        user.save()
        return True
    return False


# category and products part
@sync_to_async
def get_categories_by_parent(parent_id=None):
    return list(Category.objects.filter(parent_id=parent_id))


@sync_to_async
def get_products_by_category(category_id):
    return list(Product.objects.filter(categories=category_id))


@sync_to_async
def get_category_by_id(category_id):
    return Category.objects.get(id=category_id)


@sync_to_async
def get_child_categories(parent_category):
    return list(Category.objects.filter(parent=parent_category))


@sync_to_async
def get_back_id(parent_cat):
    return parent_cat.parent.id if parent_cat.parent else None


@sync_to_async
def get_parent_category(category):
    return category.parent


@sync_to_async
def get_root_categories():
    return list(Category.objects.filter(parent=None))


# products logic
@sync_to_async
def get_product_by_id(product_id):
    return Product.objects.get(id=product_id)


@sync_to_async
def get_product_by_product_color_id(product_color_id):
    product_color = ProductColor.objects.select_related('product').get(id=product_color_id)
    return product_color.product


@sync_to_async
def get_product_colors(product_id):
    return list(ProductColor.objects.filter(product_id=product_id).select_related('color'))


@sync_to_async
def get_product_color_by_id(color_id):
    return ProductColor.objects.select_related('color').get(id=color_id)


@sync_to_async
def get_images_for_color(color_id):
    return list(ProductImage.objects.filter(productcolor=color_id))


# basket
@sync_to_async
def add_to_basket(user_id, product_color_id):
    User = get_user_model()
    user = User.objects.get(chat_id=user_id)

    basket, _ = Basket.objects.get_or_create(user=user)
    item, created = BasketItem.objects.get_or_create(basket=basket, product_color_id=product_color_id)

    if not created:
        item.quantity += 1
        item.save()


@sync_to_async
def remove_from_basket(user_id, product_color_id):
    User = get_user_model()
    user = User.objects.get(chat_id=user_id)

    try:
        basket = Basket.objects.get(user=user)
        item = BasketItem.objects.get(basket=basket, product_color_id=product_color_id)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    except (Basket.DoesNotExist, BasketItem.DoesNotExist):
        pass


@sync_to_async
def get_basket_items(user_id):
    return list(
        BasketItem.objects.select_related(
            'product_color', 'product_color__product', 'product_color__color', 'basket', 'basket__user'
        ).filter(basket__user__id=user_id)
    )
