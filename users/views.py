import secrets
import random
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


# Create your views here.
class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()  # сохраняем пользователя
        user.is_active = False
        # генерируем токен через secrets
        token = secrets.token_hex(16)
        # сохраняем токен в базе
        user.token = token
        user.save()
        # получаем токен откуда пришел пользователь
        host = self.request.get_host()
        # сгенерировать пользователю ссылку для перехода
        url = f'http://{host}/users/email-confirm/{token}/'
        # реализуем отправку самого сообщения
        # добавим импорт from config.settings import EMAIL_HOST_USER
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, для окончания регистрации перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            # пользователь при регистрации указал почту, мы на нее отправляем
            recipient_list=[user.email],
        )
        return super().form_valid(form)


# опишем сам метод, который будет принимать урл
def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True  # была ошибка us_active
    user.save()
    return redirect(reverse('users:login'))


def password_reset(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            new_password = randompassword()
            # new_password = get_random_string(length=12)
            # print('randompassword', randompassword)
            user.password = make_password(new_password)

            # Генерировать пароль можно проще (из замечания к ДЗ 22.2 Аутентификация)
            # User.objects.make_random_password()

            # print('user.password', user.password)
            # получаем токен откуда пришел пользователь
            host = request.get_host()
            # сгенерировать пользователю ссылку для перехода
            url = f'http://{host}/users/login/'
            user.save()

            # Отправка нового пароля на почту пользователя
            send_mail(
                subject='Ваш новый пароль',
                message=f'Ваш новый пароль: {new_password}\n'
                        f'Войти с новым паролем: {url}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return redirect('password_reset_done')
        except User.DoesNotExist:
            # Если пользователь не найден, можно вернуть ошибку
            return render(request, 'password_reset.html', {'error': 'Пользователь с таким email не найден.'})

    return render(request, 'password_reset.html')


def password_reset_done(request):
    return render(request, 'password_reset_done.html')


#  создаем новый рандомный пароль для пользователя
def randompassword():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(8, 12)
    new_password = ''.join(random.choice(chars) for x in range(size))
    return new_password


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})


class UserListView(LoginRequiredMixin, ListView):
    model = User
    login_url = '/users/login/'
    template_name = 'users_list.html'

    def get_queryset(self):
        users_list = super().get_queryset()
        if self.request.user.is_staff:
            return users_list
        else:
            return PermissionDenied


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    login_url = '/users/login/'
    template_name = 'user_detail.html'
