from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, CommandHandler, filters
from asgiref.sync import sync_to_async
from main.models import BotUser


@sync_to_async
def create_or_update_user(chat_id, full_name, phone):
    return BotUser.objects.update_or_create(
        chat_id=chat_id,
        defaults={
            "name": full_name,
            "phone": phone,
        }
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ask user for contact
    contact_button = KeyboardButton("📱 Share your phone number", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Iltimos, telefon raqamingizni yuboring.\nПожалуйста, отправьте свой номер телефона.",
        reply_markup=keyboard
    )


async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if not contact:
        await update.message.reply_text("Telefon raqam topilmadi.")
        return

    telegram_id = update.effective_user.id
    full_name = update.effective_user.full_name or "No Name"
    phone = contact.phone_number

    user, created = await create_or_update_user(telegram_id, full_name, phone)

    await update.message.reply_text("Raqamingiz muvaffaqiyatli saqlandi. Botga xush kelibsiz!\nДобро пожаловать в бот!")
