from django.core.management import BaseCommand

from sending_mail.services import MailingServices


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--email", type=str, help="Email пользователя")
        parser.add_argument("--pk", type=int, help="PK рассылки")

    def handle(self, *args, **kwargs):
        email = kwargs["email"]
        pk = kwargs["pk"]
        MailingServices.send_mailing(email, pk)
