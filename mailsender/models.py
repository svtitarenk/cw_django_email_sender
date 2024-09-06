from datetime import datetime

from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """
    - почта (email)
    - Ф. И. О. (name)
    - телефон (PhoneNumberField)
    - Город
    - комментарий
    - компания (чтобы можно было включить в рассылку компанию)
    - активный или нет
    """

    email = models.EmailField(
        unique=True,
        verbose_name='email',
        help_text='Email address'
    )
    full_name = models.CharField(
        max_length=255,
        **NULLABLE,
        verbose_name='full_name',
        help_text='Введите ФИО клиента'
    )
    phone_number = PhoneNumberField(
        max_length=15,
        **NULLABLE,
        region='RU',
        verbose_name='phone_number',
        help_text='Введите телефон клиента'
    )
    city = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name='Город',
        help_text='Введите город клиента'
    )
    comment = models.TextField(
        **NULLABLE,
        verbose_name='Комментарий',
        help_text='Введите комментарий клиента'
    )
    company = models.CharField(
        max_length=100,
        **NULLABLE,
        verbose_name='компания',
        help_text='Введите компанию клиента'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='активный или нет',
        help_text='Отметьте, активен клиент или нет'
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.full_name} (email: {self.email})'


class Message(models.Model):
    subject = models.CharField(max_length=150)
    image = models.ImageField(
        upload_to='mailsender/photo',
        **NULLABLE,
        verbose_name='Изображение',
        help_text='Загрузите изображение для сообщения'
    )
    body = models.TextField()

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject


class MailingList(models.Model):
    """
    - название рассылки
    - дата и время первой отправки рассылки;
    - периодичность: раз в день, раз в неделю, раз в месяц;
    - статус рассылки (например, завершена, создана, запущена).
    - создатель рассылки
    - id_user (foreignkey)
    - FREQUENCY_CHOICES - Частота рассылки
    - STATUS_CHOICES - Статус рассылки
    """

    ONCE = 'once'
    DAILY = 'day'
    WEEKLY = 'week'
    MONTHLY = 'month'

    FREQUENCY_CHOICES = [
        (ONCE, 'Один раз'),
        (DAILY, 'Раз в день'),
        (WEEKLY, 'Раз в неделю'),
        (MONTHLY, 'Раз в месяц'),
    ]

    CREATED = 'created'
    STARTED = 'started'
    FINISHED = 'finished'

    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
        (FINISHED, 'Завершена'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="Название рассылки",
        help_text='Введите название рассылки'
    )
    start_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время первой отправки рассылки',
        help_text='Дата и время первой отправки рассылки'
    )
    end_time = models.DateTimeField(
        **NULLABLE,
        verbose_name='Дата и время окончания рассылки',
        help_text='Дата и время окончания рассылки'
    )
    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        verbose_name='Периодичность',
        help_text='Выберите периодичность'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name='Статус рассылки',
        help_text='Выберите статус рассылки'
    )
    # creator = models.ForeignKey(
    #     'auth.User',
    #     on_delete=models.CASCADE,
    #     verbose_name='Создатель рассылки',
    #     help_text='Создатель рассылки'
    # )
    """ Связь ManyToMany между MailingList и Client: Эта связь позволяет связать множество клиентов 
    с одной рассылкой для управления списками рассылок и их получателями."""
    clients = models.ManyToManyField(
        Client,
        related_name='mailing_lists'
    )
    """Связь OneToOne между MailingList и Message: Каждая рассылка должна быть связана 
    с одним конкретным сообщением, которое будет отправлено клиентам. """
    message = models.ForeignKey(
        Message,
        related_name='mailing_lists',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'{self.name}: dt: {self.start_time}, freq: {self.frequency}, status: {self.status}'


class MailingAttempt(models.Model):
    """
    - attempt_time (дата и время последней попытки): DateTimeField
    - status (статус попытки): BooleanField (успешно / не успешно)
    - response (ответ почтового сервера): TextField
    - message (связь с сообщением): ForeignKey к модели Message
    - client (связь с клиентом): ForeignKey к модели Client
    """
    attempt_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='attempt_time'
    )
    status = models.BooleanField(
        verbose_name='status'
    )
    response = models.TextField(**NULLABLE)
    message = models.ForeignKey(
        Message,
        related_name='attempts',
        on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        Client,
        related_name='attempts',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Попытка отправки сообщения'
        verbose_name_plural = 'Попытки отправки сообщений'

    def __str__(self):
        return f"Attempt for {self.client.email} at {self.attempt_time}"
