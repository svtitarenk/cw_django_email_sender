import pytz
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from mailsender.models import MailingList, MailingAttempt
from django.utils import timezone


# Функция старта периодических задач
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=60)
    scheduler.start()
    scheduler.print_jobs()


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    # Фильтрация активных рассылок
    mailings = MailingList.objects.filter(
        start_time__lte=current_datetime,
        end_time__gte=current_datetime,
        status__in=['created', 'started']
    )
    # print('mailings', mailings)
    # print('current_datetime', current_datetime)
    # print('zone', zone)
    attempts = MailingAttempt.objects.all()

    for mailing in mailings:
        last_attempt = MailingAttempt.objects.filter(mailing=mailing).order_by('attempt_time').first()
        next_send_time = current_datetime + timedelta(days=1)

        print('------------------------------------------------------------------------')
        print('mailing: ', mailing)
        print('last_attempt: ', last_attempt)
        print('mailing.frequency: ', mailing.frequency)

        # Определение времени следующей отправки на основе частоты
        if mailing.frequency == 'once':
            if not last_attempt:
                next_send_time = mailing.start_time
                print('once - next_send_time: ', next_send_time)
            else:
                break
        elif mailing.frequency == 'day' and (
                not last_attempt or (current_datetime - last_attempt.attempt_time).days >= 1):
            next_send_time = last_attempt.attempt_time + timedelta(
                days=1,
                hours=last_attempt.time.hours,
                minutes=last_attempt.time.minute
            ) if last_attempt else mailing.start_time
            print('day - next_send_time: ', next_send_time)
        elif mailing.frequency == 'week' and (
                not last_attempt or (current_datetime - last_attempt.attempt_time).days >= 7):
            next_send_time = last_attempt.attempt_time + timedelta(
                weeks=1,
                hours=last_attempt.time.hours,
                minutes=last_attempt.time.minute
            ) if last_attempt else mailing.start_time
            print('week - next_send_time: ', next_send_time)
        elif mailing.frequency == 'month' and (
                not last_attempt or (current_datetime - last_attempt.attempt_time).days >= 30):
            next_send_time = last_attempt.attempt_time + timedelta(
                days=30,
                hours=last_attempt.time.hours,
                minutes=last_attempt.time.minute
            ) if last_attempt else mailing.start_time
            print('month - next_send_time: ', next_send_time)

        print('current_datetime: ', current_datetime)
        print('next_send_time: ', next_send_time)
        print('next_send_time <= current_datetime: ', next_send_time <= current_datetime)
        if next_send_time <= current_datetime:
            # Отправляем письма всем клиентам рассылки
            for client in mailing.clients.filter(is_active=True):
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email]
                    )
                    # Меняем статус рассылки
                    if mailing.frequency == 'once':
                        mailing.status = 'finished'
                        mailing.save()
                    else:
                        mailing.status = 'started'
                        mailing.save()
                    # Логируем успешную отправку
                    MailingAttempt.objects.create(
                        status=True,
                        message=mailing.message,
                        client=client,
                        response="Message sent successfully",
                        mailing=mailing,
                        attempt_time=timezone.now()  # Сохраняем текущее время отправки
                    )
                except Exception as e:
                    # Логируем неудачную отправку
                    MailingAttempt.objects.create(
                        status=False,
                        message=mailing.message,
                        client=client,
                        mailing=mailing,
                        response=str(e),
                        attempt_time=timezone.now()  # Сохраняем текущее время отправки
                    )
