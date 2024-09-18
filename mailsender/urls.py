from django.urls import path
from django.views.decorators.cache import cache_page

# импортируем название приложения
from mailsender.apps import MailsenderConfig
from mailsender.views import MailsenderListView, MailingListListView, ClientListListView, \
    ClientDetailView, MailingListDetailView, index, MailingListCreateView, MailingListUpdateView, MailingListDeleteView, \
    ClientUpdateView, ClientDeleteView, ClientCreateView, MailingAttemptListView, MessageListView, MessageDetailView, \
    MessageCreateView, MessageUpdateView, MessageDeleteView

# создаем переменную с названием приложения
app_name = MailsenderConfig.name

# urls mailsender
urlpatterns = [
    path('', index, name='mailsender_list'),
    path('mailinglist/', cache_page(60)(MailingListListView.as_view()), name='mailinglist'),
    path('mailinglist/<int:pk>/', MailingListDetailView.as_view(), name='mailinglist_detail'),
    path('mailinglist/create/', MailingListCreateView.as_view(), name='mailinglist_create'),
    path('mailinglist/<int:pk>/update/', MailingListUpdateView.as_view(), name='mailinglist_update'),
    path('mailinglist/<int:pk>/delete/', MailingListDeleteView.as_view(), name='mailinglist_delete'),

    path('client/', ClientListListView.as_view(), name='client'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('mailingattempt/', MailingAttemptListView.as_view(), name='mailingattempt'),

    path('message/', MessageListView.as_view(), name='message'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
]
