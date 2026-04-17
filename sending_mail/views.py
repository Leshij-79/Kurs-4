from django.shortcuts import render
from django.views.generic import ListView

from sending_mail.models import Mailing


class MailingListView(ListView):
    model = Mailing
