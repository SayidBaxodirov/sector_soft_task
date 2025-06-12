from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from django.conf import settings
from bot.handlers import start, contact_handler, language_command, language_selection, text_handler, \
    category_callback_handler, color_callback_handler, basket_callback_handler


def main():
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("language", language_command))
    app.add_handler(MessageHandler(filters.Regex("^(🇺🇿 Uzbek|🇷🇺 Russian)$"), language_selection))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(CallbackQueryHandler(color_callback_handler, pattern=r"^color_\d+$"))
    app.add_handler(CallbackQueryHandler(basket_callback_handler, pattern=r"^(add|remove)_\d+$"))
    app.add_handler(CallbackQueryHandler(category_callback_handler))
    app.run_polling()
