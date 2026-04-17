from django.urls import path

from sending_mail.apps import SendingMailConfig
from sending_mail.views import MailingListView

app_name = SendingMailConfig.name

urlpatterns = [
    path("", MailingListView.as_view(), name="mailing_list"),
]