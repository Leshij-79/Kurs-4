from django.urls import path

from sending_mail.apps import SendingMailConfig
from sending_mail.views import MessagesListView, MessageDetailView, MessageCreateView, \
    MessageUpdateView, MessageDeleteView, RecipientsListView, RecipientDetailView, RecipientUpdateView, \
    RecipientCreateView, RecipientDeleteView, IndexListView, MailingListView, MailingDetailView, \
    MailingUpdateView, MailingCreateView, MailingDeleteView

app_name = SendingMailConfig.name

urlpatterns = [
    path("", IndexListView.as_view(), name="index"),
    path("messages/", MessagesListView.as_view(), name="messages_list"),
    path("messages/message_detail/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("messages/message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("messages/message_create/", MessageCreateView.as_view(), name="message_create"),
    path("messages/message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
    path("recipients/", RecipientsListView.as_view(), name="recipients_list"),
    path("recipients/recipient_detail/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipients/recipient_update/<int:pk>/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipients/recipient_create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipients/recipient_delete/<int:pk>/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path("mailing/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/mailing_detail/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/mailing_update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/mailing_create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/mailing_delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
]