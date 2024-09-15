from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона"
    )
    avatar = models.ImageField(
        upload_to="users/avatar/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар пользователя"
    )
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
        blank=True,
        null=True,
        help_text="Введите страну пользователя"
    )
    token = models.CharField(
        max_length=100,
        verbose_name="Токен",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='активный или нет',
        help_text='Отметьте, активен клиент или нет'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

        permissions = [
            ("can_edit_is_active", "Can edit is_active"),  # описываем как будет называться в админке
        ]

    def __str__(self):
        return f'{self.email}'
