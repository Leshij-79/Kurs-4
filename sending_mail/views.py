
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from sending_mail.forms import (MailingCUForm, MailingDetailForm, MailingStatForm, MessageCUForm, MessageDetailForm,
                                RecipientCUForm, RecipientDetailForm)
from sending_mail.models import Mailing, Messages, Recipients, WorkMailing
from sending_mail.services import (IndexServices, MailingServices, MailingStatServices, MessagesServices,
                                   RecipientsServices, get_index_cached, get_messages_cached)


class IndexListView(ListView):
    model = Mailing
    template_name = "index.html"

    def get_queryset(self):
        return get_index_cached("index", 60)

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

    def get_queryset(self):
        return Messages.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        owner_id = self.request.user
        context["all_messages"] = MessagesServices.all_messages(owner_id)

        cached_value = get_messages_cached("messageslist", 60)
        context["cached_data"] = cached_value

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

    @method_decorator(cache_page(60, key_prefix="recipients:list"), name="r_list")
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_authenticated and not user.groups.filter(name="Moderator").exists():
            return Recipients.objects.filter(owner=user)

        if user.is_authenticated and user.groups.filter(name="Moderator").exists():
            return queryset

        return self.model.objects.none()

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


@method_decorator(cache_page(60), name="dispatch")
class MailingListView(ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "all_mailing"
    success_url = reverse_lazy("sending_mail:index")

    def get_queryset(self):

        user = self.request.user
        queryset = super().get_queryset()

        if user.is_authenticated and not user.groups.filter(name="Moderator").exists():
            return Mailing.objects.filter(owner=user)

        if user.is_authenticated and user.groups.filter(name="Moderator").exists():
            return queryset

        return self.model.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        owner_id = self.request.user
        context["all_mailing"] = MailingServices.all_mailing(owner_id)

        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    context_object_name = "mailing"
    form_class = MailingDetailForm
    template_name = "mailing/mailing_detail.html"
    success_url = reverse_lazy("sending_mail:mailing_list")

    def get_object(self, queryset=None):
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


class MailingSendView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        email_owner = self.request.user.email

        MailingServices.send_mailing(email_owner, pk)

        messages.success(request, f'Рассылка "{mailing.pk}" была запущена.')
        return redirect("sending_mail:mailing_detail", pk=mailing.pk)


class MailingStatView(LoginRequiredMixin, ListView):
    model = WorkMailing
    form_class = MailingStatForm
    template_name = "mailing/mailing_statistic.html"
    success_url = reverse_lazy("sending_mail:index")

    def get_queryset(self):
        return WorkMailing.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        owner_id = self.request.user
        context["all_mailing"] = MailingStatServices.all_mailing(owner_id)

        return context


def mailing_diactive(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.end_time = timezone.now()
    mailing.is_active = False
    mailing.save()
    return redirect(reverse("sending_mail:mailing_detail", args=[pk]))
