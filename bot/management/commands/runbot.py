from django.core.management.base import BaseCommand
from bot.bot import main  # botni boshlash funksiyasi


class Command(BaseCommand):
    help = "Start the telegram bot"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting the Telegram bot..."))
        try:
            main()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Bot stopped with error: {e}"))
        else:
            self.stdout.write(self.style.SUCCESS("Telegram bot stopped successfully."))
