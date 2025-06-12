from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup

from .db import get_categories_by_parent, get_products_by_category, get_category_by_id, get_back_id, get_product_by_id, \
    get_product_colors

choose_lang = {
    "uz": "Yangi tilni tanlang:",
    "ru": "Выберите новый язык:"
}
lang_changed = {
    "uz": "Til muvaffaqiyatli o‘zgartirildi ✅",
    "ru": "Язык успешно изменен ✅"
}
send_phone_btn = {
    "uz": "📱 Telefon raqamni yuborish",
    "ru": "📱 Отправить номер телефона"
}
send_phone = {
    "uz": "Iltimos, telefon raqamingizni yuboring.",
    "ru": "Пожалуйста, отправьте свой номер телефона."
}
phone_saved = {
    "uz": "Raqamingiz saqlandi. Botga xush kelibsiz!",
    "ru": "Ваш номер сохранен. Добро пожаловать в бот!"
}
menu_txt = {
    'uz': [["📚 Kategoriyalar", "🛒 Savatcha"]],
    'ru': [["📚 Категории", "🛒 Корзина"]]
}
categories = {
    'uz':"📚 Kategoriyalar",
    'ru':'📚 Категории'
}
category_txt = {
    'uz': "📂 Kategoriyalar ro'yxati:",
    'ru': "📂 Список категорий:"
}
basket_txt = {
    "uz": "🛒 Savatcha",
    'ru': "🛒 Корзина"
}


def menu(language):
    if language == 'uz':
        keyboard = [["📚 Kategoriyalar", "🛒 Savatcha"]]
    elif language == 'ru':
        keyboard = [["📚 Категории", "🛒 Корзина"]]
    else:
        keyboard = [["📚 Kategoriyalar", "🛒 Savatcha"]]  # default

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


async def build_category_keyboard(category_id=None, lang='uz'):
    categories = await get_categories_by_parent(category_id)

    if categories:
        keyboard = [
            [InlineKeyboardButton(
                getattr(cat, f"{lang}_name"), callback_data=f"category_{cat.id}"
            )] for cat in categories
        ]
    else:
        # ichida boshqa kategoriya bo'lmasa mahsulotlarni jo'natish
        products = await get_products_by_category(category_id)
        keyboard = [
            [InlineKeyboardButton(
                getattr(prod, f"{lang}_name"), callback_data=f"product_{prod.id}"
            )] for prod in products
        ]

    # orqaga logic
    if category_id:
        parent_cat = await get_category_by_id(category_id)
        back_id = await get_back_id(parent_cat)
        keyboard.append([InlineKeyboardButton("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
                                              callback_data=f"category_{back_id if back_id else 'root'}")])

    return InlineKeyboardMarkup(keyboard)


async def send_product_details(update, context, product_id, lang):
    product = await get_product_by_id(product_id)
    colors = await get_product_colors(product_id)
    keyboard = [
        [InlineKeyboardButton(f"{color.color.name} - ${color.price}", callback_data=f"color_{color.id}")]
        for color in colors
    ]
    markup = InlineKeyboardMarkup(keyboard)


    caption = f"🛍 {getattr(product, f'{lang}_name')}\n\n{getattr(product, f'{lang}_description')}"

    with open(product.main_image.path, 'rb') as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=caption,
            reply_markup=markup
        )
