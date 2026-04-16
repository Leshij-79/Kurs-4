from django.contrib import admin

from sending_mail.models import Recipients, Messages, Mailing, WorkMailing


@admin.register(Recipients)
class RecipientsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "comment",
        "owner",
    )

    list_filter = ("name",)

    search_fields = (
        "name",
        "email",
    )


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "mail_body",
        "owner",
    )

    list_filter = ("subject",)

    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "message",
        "status",
        "start_time",
        "end_time",
        "owner",
    )

    list_filter = ("message",)

    search_fields = ("message",)


@admin.register(WorkMailing)
class WorkMailingAdmin(admin.ModelAdmin):
    list_display = (
        "mailing",
        "attempt_time",
        "status",
        "server_response",
    )

    list_filter = ("mailing",)

    search_fields = ("mailing",)
