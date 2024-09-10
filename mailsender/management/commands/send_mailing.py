from django.core.management.base import BaseCommand
from mailsender.services import send_mailing


class Command(BaseCommand):
    help = 'Send mailing to clients'

    def handle(self, *args, **kwargs):
        send_mailing()
        self.stdout.write(self.style.SUCCESS('Mailing successfully sent!'))
