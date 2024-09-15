from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from mailsender.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")
        # exclude = ('views_counter',)


class UserProfileForm(UserChangeForm):
    password = None  # исключаем поле пароля из формы

    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar', 'is_active',)


class UserProfileModeratorForm(UserChangeForm):
    password = None  # исключаем поле пароля из формы

    class Meta:
        model = User
        fields = ('is_active',)

