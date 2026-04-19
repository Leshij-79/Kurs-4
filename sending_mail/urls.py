from django.urls import path

from sending_mail.apps import SendingMailConfig
from sending_mail.views import MailingListView, MessagesListView, MessageDetailView, MessageCreateView, \
    MessageUpdateView, MessageDeleteView

app_name = SendingMailConfig.name

urlpatterns = [
    path("", MailingListView.as_view(), name="mailing_list"),
    path("messages/", MessagesListView.as_view(), name="messages_list"),
    path("messages/message_detail/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("messages/message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("messages/message_create/", MessageCreateView.as_view(), name="message_create"),
    path("messages/message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),

]