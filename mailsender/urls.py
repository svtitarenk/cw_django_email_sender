from django.urls import path
# импортируем название приложения
from mailsender.apps import MailsenderConfig

# создаем переменную с названием приложения
app_name = MailsenderConfig.name

# урлы пока оставляем пусты
urlpatterns = [
    # path('', 'mailsender:mailsender_list', name='mailsender_list'),
    # path('<int:pk>/', 'mailsender:mailsender_detail', name='mailsender_detail'),
    # path('create/', 'mailsender:mailsender_create', name='mailsender_create'),
]
