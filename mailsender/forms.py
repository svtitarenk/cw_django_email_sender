from django.forms import BooleanField, ModelForm, DateTimeField
from django import forms
from mailsender.models import MailingList, Client


class StyleFormMixin:
    # переопределяем инициализацию формы, чтобы сделать форму с определенным стилем
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # необходимо сделать цикл, в котором будем изменять стили полей
        for field_name, field in self.fields.items():
            # можем сделать проверку
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class MailingListForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingList
        # start_time_filed = DateTimeField(widget=DateTimeField)
        fields = ('name', 'start_time', 'end_time',  'frequency', 'message', "clients",)
        # fields = "__all__"
        # exclude = ('views_counter', 'owner')

        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        # start_time_filed = DateTimeField(widget=DateTimeField)
        # fields = ('name', 'start_time', 'frequency', 'message', "clients",)
        fields = "__all__"

