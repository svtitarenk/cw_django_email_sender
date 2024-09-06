from django.contrib import admin

from mailsender.models import Client, MailingList, Message, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "phone_number", "city", "company", "is_active")
    # list_filter = ("name", "email", "address")
    search_fields = ("email", "full_name", "is_active")


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "start_time", "frequency", "status",)
    list_filter = ("name", "start_time", "status",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "body")
    list_filter = ("subject", "body",)


@admin.register(MailingAttempt)
class MMailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt_time", "status", "message", "client",)
    list_filter = ("client", "status",)
