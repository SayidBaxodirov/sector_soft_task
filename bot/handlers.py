from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from .db import get_user_by_chat_id, create_or_update_user, update_user_language, get_category_by_id, \
    get_child_categories, get_products_by_category, get_parent_category, get_root_categories, get_product_by_id, \
    get_product_color_by_id, get_images_for_color, add_to_basket, remove_from_basket, get_product_by_product_color_id, \
    get_basket_items
from .keyboards import menu_txt, choose_lang, lang_changed, send_phone, send_phone_btn, phone_saved, menu, category_txt, \
    build_category_keyboard, basket_txt, send_product_details, categories


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    user = await get_user_by_chat_id(chat_id)

    if user:
        await update.message.reply_text({
                                            "uz": f"Assalomu alaykum {user.name}.\nXush kelibsiz!",
                                            "ru": f"Здравствуйте {user.name}.\nДобро пожаловать!"
                                        }.get(user.language, "Assalomu alaykum!"), reply_markup=menu(user.language))
        return

    lang_buttons = [[KeyboardButton("🇺🇿 Uzbek"), KeyboardButton("🇷🇺 Russian")]]
    keyboard = ReplyKeyboardMarkup(lang_buttons, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("Tilni tanlang / Выберите язык:", reply_markup=keyboard)


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    user = await get_user_by_chat_id(chat_id)

    if not user:
        await update.message.reply_text(
            "Birinchi /start orqali registratsiyadan o'ting\nПожалуйста зарегистрируйтесь с помощью /start.")
        return

    lang_buttons = [[KeyboardButton("🇺🇿 Uzbek"), KeyboardButton("🇷🇺 Russian")]]
    keyboard = ReplyKeyboardMarkup(lang_buttons, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(choose_lang.get(user.language, "Choose a new language:"), reply_markup=keyboard)

    context.user_data["changing_language"] = True


async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    language = "uz" if "Uzbek" in text else "ru" if "Russian" in text else None

    if not language:
        await update.message.reply_text("Iltimos, quyidagi tugmalardan birini tanlang.")
        return

    chat_id = update.effective_user.id

    if context.user_data.get("changing_language"):
        updated = await update_user_language(chat_id, language)
        await update.message.reply_text(lang_changed.get(language, "Language changed successfully ✅"),
                                        reply_markup=menu(language))

        context.user_data["changing_language"] = False
        return

    # Not changing language: continue registration
    context.user_data["language"] = language

    contact_btn = KeyboardButton(send_phone_btn[language], request_contact=True)

    keyboard = ReplyKeyboardMarkup([[contact_btn]], resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(send_phone[language], reply_markup=keyboard)


async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    chat_id = update.effective_user.id
    full_name = update.effective_user.full_name
    phone = contact.phone_number
    language = context.user_data.get("language", "uz")

    await create_or_update_user(chat_id, full_name, phone, language)

    await update.message.reply_text(phone_saved[language], reply_markup=menu(language))


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_user.id
    user = await get_user_by_chat_id(chat_id)
    if text in categories.get(user.language, []):
        await update.message.reply_text(
            category_txt[user.language],
            reply_markup=await build_category_keyboard(lang=user.language)
        )
    elif text in basket_txt.get(user.language, []):
        # Get basket items from DB
        basket_items = await get_basket_items(user.id)

        if not basket_items:
            await update.message.reply_text({
                                                'uz': "🛒 Savatchangiz hozircha bo‘sh.",
                                                'ru': "🛒 Ваша корзина пуста."
                                            }[user.language])
            return

        # Format basket message
        message_lines = []
        for item in basket_items:
            product_name = getattr(item.product_color.product, f"{user.language}_name", "Noma'lum")
            color_name = item.product_color.color.name
            price = item.product_color.price
            message_lines.append(f"🛍 {product_name} - 🎨 {color_name} - 💵 ${price}")

        basket_text = "\n\n".join(message_lines)
        await update.message.reply_text(
            f"🛒 {'Savatchangizdagilar' if user.language == 'uz' else 'Товары в корзине'}:\n\n{basket_text}"
        )


async def category_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user = query.from_user
    user_data = await get_user_by_chat_id(user.id)
    lang = user_data.language

    if data == "home" or data == "category_root":
        keyboard = await build_category_keyboard(category_id=None, lang=lang)
        await query.edit_message_text(
            text=category_txt[lang],
            reply_markup=keyboard
        )
        return

    if data.startswith("category_"):
        category_id = data.split("_")[1]
        category_id = int(category_id) if category_id != 'root' else None

        keyboard = await build_category_keyboard(category_id=category_id, lang=lang)
        await query.edit_message_text(
            text=category_txt[lang],
            reply_markup=keyboard
        )

    elif data.startswith("product_"):
        product_id = int(data.split("_")[1])
        await send_product_details(update, context, product_id, lang)


async def color_callback_handler(update, context):
    query = update.callback_query
    await query.answer()
    user_data = await get_user_by_chat_id(query.from_user.id)
    language = user_data.language
    color_id = int(query.data.split("_")[1])
    color = await get_product_color_by_id(color_id)
    images = await get_images_for_color(color_id)
    product = await get_product_by_product_color_id(color_id)

    if not images:
        await query.message.reply_text("No images found for this color.")
        return

    # 1. rasmlarni jo'natish
    media_group = []
    for i, image in enumerate(images[:10]):
        with open(image.image.path, 'rb') as img_file:
            media = InputMediaPhoto(
                media=img_file.read(),
                caption=(
                    f"🛍 {getattr(product, f'{language}_name')}\n🎨 {color.color.name}\n💵 ${color.price}" if i == 0 else None
                )
            )
            media_group.append(media)

    await context.bot.send_media_group(
        chat_id=query.message.chat.id,
        media=media_group
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕", callback_data=f"add_{color.id}"),
            InlineKeyboardButton("➖", callback_data=f"remove_{color.id}")
        ],
        [
            InlineKeyboardButton("⬅️ Orqaga" if language == "uz" else "⬅️ Назад", callback_data=f"product_{product.id}")
        ]
    ])
    text = f"🛍 {product.uz_name} - {color.color.name}\n💵 Narx: ${color.price}" if language == "uz" else f"🛍 {product.ru_name} - {color.color.name}\n💵 Стоимость: ${color.price}"
    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text=text,
        reply_markup=keyboard
    )


async def basket_callback_handler(update, context):
    query = update.callback_query
    await query.answer()
    user_data = await get_user_by_chat_id(query.from_user.id)
    lang = user_data.language
    data = query.data
    action, color_id = data.split("_")
    color_id = int(color_id)

    if action == "add":
        await add_to_basket(user_id=query.from_user.id, product_color_id=color_id)
        await query.edit_message_text(
            "✅ Mahsulot savatga qo'shildi" if lang == "uz" else "✅ Продукт добавлен в корзину")
    elif action == "remove":
        await remove_from_basket(user_id=query.from_user.id, product_color_id=color_id)
        await query.edit_message_text(
            "🗑 Mahsulot savatdan olib tashlandi" if lang == "uz" else "🗑 Продукт убран из корзины")
