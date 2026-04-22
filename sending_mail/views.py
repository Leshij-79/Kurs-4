from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailAttachment, send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.models import AnonymousUser

from config import settings
from sending_mail.forms import MessageDetailForm, MessageCUForm, RecipientDetailForm, RecipientCUForm, MailingCUForm, \
    MailingDetailForm
from sending_mail.models import Mailing, Messages, Recipients, WorkMailing
from sending_mail.services import MessagesServices, RecipientsServices, MailingServices, IndexServices


class IndexListView(ListView):
    model = Mailing
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner_id = self.request.user

        if isinstance(owner_id, AnonymousUser):
            context["all_mailing_user"] = []
            context["all_recipients_user"] = []
            context["active_mailings_user"] = []
        else:
            context["all_mailing_user"] = IndexServices.calculate_all_mailings_user(owner_id)
            context["all_recipients_user"] = IndexServices.calculate_all_recipients_user(owner_id)
            context["active_mailings_user"] = IndexServices.calculate_active_mailings_user(owner_id)

        context["all_mailing"] = IndexServices.calculate_all_mailings()
        context["all_recipients"] = IndexServices.calculate_all_recipients()
        context["active_mailings"] = IndexServices.calculate_active_mailings()

        return context


class MessagesListView(ListView):
    model = Messages
    template_name = "messages/messages_list.html"
    context_object_name = "all_messages"
    success_url = reverse_lazy("sending_mail:index")

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
    success_url = reverse_lazy("sending_mail:index")

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
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
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


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "all_mailing"
    success_url = reverse_lazy("sending_mail:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        owner_id = self.request.user
        context["all_mailing"] = MailingServices.all_mailing(owner_id)

        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    form_class = MailingDetailForm
    template_name = "mailing/mailing_detail.html"
    success_url = reverse_lazy("sending_mail:mailing_list")

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingCUForm
    template_name = "mailing/mailing_cu.html"
    success_url = reverse_lazy("sending_mail:mailing_list")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingCUForm
    template_name = "mailing/mailing_cu.html"
    success_url = reverse_lazy("sending_mail:mailing_list")

    def get_success_url(self):
        return reverse("sending_mail:mailing_detail", args=[self.kwargs.get("pk")])


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_delete.html"
    success_url = reverse_lazy("sending_mail:mailing_list")


class MailingStartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        recipients = mailing.recipients.all()


        for recipient in recipients:
            email_attempt = WorkMailing(mailing=mailing)
            email_attempt.attempt_time = timezone.now()
            email_attempt.owner = self.request.user
            email_attempt.recipient = recipient

            server_response = send_mail(
                subject=f"mailing.message.subject",
                message=f"mailing.message.mail_body",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
            )

