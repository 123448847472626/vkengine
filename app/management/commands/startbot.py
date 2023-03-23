from django.core.management.base import BaseCommand
from app.bot.app import VkBot


class Command(BaseCommand):
    help = 'Start VkBot'

    def handle(self, *args, **options):
        current_bot = VkBot()