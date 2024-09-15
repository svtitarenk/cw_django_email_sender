from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from mailsender.forms import MailingListForm, ClientForm, MailingListModeratorForm, MessageForm
from mailsender.models import MailingList, Client, MailingAttempt, Message


def index(request):
    mailing_list = MailingList.objects.all()
    context = {
        'object_list': mailing_list,
        'title': 'Главная'
    }
    return render(request, 'mailsender/mailsender_dashboard.html', context)


"""
-------------------------------------------------------------------------------
Mailings views
"""


class MailsenderListView(LoginRequiredMixin, ListView):
    model = MailingList
    template_name = 'mailsender/index.html'
    login_url = '/users/login/'


class MailingListListView(LoginRequiredMixin, ListView):
    model = MailingList
    login_url = '/users/login/'

    def get_queryset(self):
        mailing = super().get_queryset()
        if self.request.user.is_staff:
            return mailing
        else:
            return mailing.filter(owner=self.request.user)


class MailingListDetailView(LoginRequiredMixin, DetailView):
    model = MailingList
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        print(context_data.get('mailinglist').pk)
        print(context_data.get('pk'))
        return context_data


class MailingListCreateView(LoginRequiredMixin, CreateView):
    model = MailingList
    login_url = '/users/login/'
    form_class = MailingListForm
    # fields = ('name', 'start_time', 'frequency', 'message', "clients",)
    success_url = reverse_lazy('mailsender:mailinglist')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = MailingList(owner=self.request.user)
        return kwargs

    # определяем рассылку к User
    def form_valid(self, form):
        mailinglist = form.save()  # сохраняем форму собаки
        # получаем пользователя из запроса.
        # можно сделать так, чтобы владелец был только авторизованный пользователь.
        # это можно сделать через LoginRequiredMixin, добавляем к классу
        # авторизованного пользователя можно получить
        user = self.request.user
        mailinglist.owner = user
        mailinglist.save()
        return super().form_valid(form)


class MailingListUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingList
    login_url = '/users/login/'
    form_class = MailingListForm
    success_url = reverse_lazy('mailsender:mailinglist')

    def get_success_url(self):
        return reverse_lazy('mailsender:mailinglist_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        # получаем пользователя
        user = self.request.user
        # прописываем проверку
        if user == self.object.owner:
            return MailingListForm
        # проверяем права, которые описали сами в модели mailsender/models.py [permissions]
        # если да, тогда возвращаем новую форму для модератора
        if user.has_perm("mailsender.can_edit_status"):
            return MailingListModeratorForm
        raise PermissionDenied


class MailingListDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingList
    login_url = '/users/login/'
    success_url = reverse_lazy('mailsender:mailinglist')


"""
-------------------------------------------------------------------------------
Clients Views
"""


class ClientListListView(LoginRequiredMixin, ListView):
    model = Client
    login_url = '/users/login/'

    def get_queryset(self):
        clients = super().get_queryset()
        if self.request.user.is_staff:
            return clients
        else:
            return clients.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    login_url = '/users/login/'
    form_class = ClientForm
    success_url = reverse_lazy('mailsender:client')

    # определяем рассылку к User
    def form_valid(self, form):
        client = form.save()  # сохраняем форму собаки
        # получаем пользователя из запроса.
        # можно сделать так, чтобы владелец был только авторизованный пользователь.
        # это можно сделать через LoginRequiredMixin, добавляем к классу
        # авторизованного пользователя можно получить
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    login_url = '/users/login/'


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    login_url = '/users/login/'
    form_class = ClientForm
    success_url = reverse_lazy('mailsender:client')

    def get_success_url(self):
        return reverse_lazy('mailsender:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    login_url = '/users/login/'
    success_url = reverse_lazy('mailsender:client')


"""
MailingAttempts CRUD -------------------------------------------------------------------------
"""


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    login_url = '/users/login/'


"""
Message CRUD -------------------------------------------------------------------------
"""


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    login_url = '/users/login/'


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    login_url = '/users/login/'

    def get_queryset(self):
        messages = super().get_queryset()
        if self.request.user.is_staff:
            return messages
        else:
            return messages.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    login_url = '/users/login/'


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    login_url = '/users/login/'
    form_class = MessageForm
    success_url = reverse_lazy('mailsender:message')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    login_url = '/users/login/'
    success_url = reverse_lazy('mailsender:message')
