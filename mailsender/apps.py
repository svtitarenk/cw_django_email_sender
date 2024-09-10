from time import sleep

from django.apps import AppConfig


class MailsenderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailsender'
    verbose_name = 'Рассылка сообщений'

    def ready(self):
        from mailsender.services import start
        sleep(2)
        start()
