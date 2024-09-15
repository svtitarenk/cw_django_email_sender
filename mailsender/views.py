from django.contrib.admin.widgets import AdminDateWidget
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from mailsender.forms import MailingListForm, ClientForm
from mailsender.models import MailingList, Client, MailingAttempt


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


class MailsenderListView(ListView):
    model = MailingList
    template_name = 'mailsender/index.html'


class MailingListListView(ListView):
    model = MailingList


class MailingListDetailView(DetailView):
    model = MailingList

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        print(context_data.get('mailinglist').pk)
        print(context_data.get('pk'))
        return context_data


class MailingListCreateView(CreateView):
    model = MailingList
    form_class = MailingListForm
    # fields = ('name', 'start_time', 'frequency', 'message', "clients",)
    success_url = reverse_lazy('mailsender:mailinglist')


class MailingListUpdateView(UpdateView):
    model = MailingList
    form_class = MailingListForm
    success_url = reverse_lazy('mailsender:mailinglist')

    def get_success_url(self):
        return reverse_lazy('mailsender:mailinglist_detail', args=[self.kwargs.get('pk')])


class MailingListDeleteView(DeleteView):
    model = MailingList
    success_url = reverse_lazy('mailsender:mailinglist')


"""
-------------------------------------------------------------------------------
Clients Views
"""


class ClientListListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailsender:client')


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailsender:client')

    def get_success_url(self):
        return reverse_lazy('mailsender:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailsender:client')


class MailingAttemptListView(ListView):
    model = MailingAttempt
