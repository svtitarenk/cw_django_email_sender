from django.contrib import admin

from mailsender.models import Client, MailingList, Message, MailingAttempt
from django_apscheduler.models import DjangoJob, DjangoJobExecution


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
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt_time", "status", "message", "client", "mailing", "response")
    list_filter = ("client", "status",)


# @admin.register(DjangoJob)
# class DjangoJobAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "job_type", "enabled", "last_run_at", "next_run_at", "total_run_count", "description")
#
#
# @admin.register(DjangoJobExecution)
# class DjangoJobExecutionAdmin(admin.ModelAdmin):
#     list_display = ("id", "job", "execution_time", "success", "traceback")
