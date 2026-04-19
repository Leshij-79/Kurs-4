from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from sending_mail.models import Mailing, Messages
from sending_mail.services import MessagesServices


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing_list.html"


class MessagesListView(ListView):
    model = Messages
    template_name = "messages_list.html"
    context_object_name = "all_messages"
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        owner_id = self.object.owner
        context["all_messages"] = MessagesServices.all_messages(owner_id)

        return context


