from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from sending_mail.forms import MessageDetailForm, MessageCUForm, RecipientDetailForm, RecipientCUForm
from sending_mail.models import Mailing, Messages, Recipients
from sending_mail.services import MessagesServices, RecipientsServices


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing_list.html"


class MessagesListView(ListView):
    model = Messages
    template_name = "messages/messages_list.html"
    context_object_name = "all_messages"
    success_url = reverse_lazy("sending_mail:mailing_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        owner_id = self.request.user
        context["all_messages"] = MessagesServices.all_messages(owner_id)

        return context


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Messages
    form_class = MessageDetailForm
    template_name = "messages/message_detail.html"
    success_url = reverse_lazy("sending_mail:messages_list")


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Messages
    form_class = MessageCUForm
    template_name = "messages/message_cu.html"
    success_url = reverse_lazy("sending_mail:messages_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Messages
    form_class = MessageCUForm
    template_name = "messages/message_cu.html"
    success_url = reverse_lazy("sending_mail:messages_list")

    def get_success_url(self):
        return reverse("sending_mail:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Messages
    template_name = "messages/message_delete.html"
    success_url = reverse_lazy("sending_mail:messages_list")


class RecipientsListView(ListView):
    model = Recipients
    template_name = "recipients/recipients_list.html"
    context_object_name = "all_recipients"
    success_url = reverse_lazy("sending_mail:mailing_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        owner_id = self.request.user
        context["all_recipients"] = RecipientsServices.all_recipients(owner_id)

        return context


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipients
    form_class = RecipientDetailForm
    template_name = "recipients/recipient_detail.html"
    success_url = reverse_lazy("sending_mail:recipients_list")


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipients
    form_class = RecipientCUForm
    template_name = "recipients/recipient_cu.html"
    success_url = reverse_lazy("sending_mail:recipients_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipients
    form_class = RecipientCUForm
    template_name = "recipients/recipient_cu.html"
    success_url = reverse_lazy("sending_mail:recipients_list")

    def get_success_url(self):
        return reverse("sending_mail:recipient_detail", args=[self.kwargs.get("pk")])


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipients
    template_name = "recipients/recipient_delete.html"
    success_url = reverse_lazy("sending_mail:recipients_list")
