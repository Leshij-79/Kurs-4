from django.utils import timezone

from sending_mail.models import Messages, Recipients, Mailing, WorkMailing


class MessagesServices:

    @staticmethod
    def all_messages(owner_id):
        messages = Messages.objects.filter(owner=owner_id)

        if not messages.exists():
            return None

        return messages


class RecipientsServices:

    @staticmethod
    def all_recipients(owner_id):
        recipients = Recipients.objects.filter(owner=owner_id)

        if not recipients.exists():
            return None

        return recipients


class MailingServices:

    @staticmethod
    def all_mailing(owner_id):
        mailing = Mailing.objects.filter(owner=owner_id)

        if not mailing.exists():
            return None

        return mailing


class IndexServices:
    @staticmethod
    def calculate_all_mailings_user(owner_id):
        mailing = Mailing.objects.filter(owner=owner_id)

        return mailing.count() if mailing.exists() else 0

    @staticmethod
    def calculate_all_mailings():
        mailing = Mailing.objects.all()

        return mailing.count() if mailing.exists() else 0

    @staticmethod
    def calculate_all_recipients_user(owner_id):
        recipients = Recipients.objects.filter(owner=owner_id)

        return recipients.count() if recipients.exists() else 0

    @staticmethod
    def calculate_all_recipients():
        recipients = Recipients.objects.all()

        return recipients.count() if recipients.exists() else 0

    @staticmethod
    def calculate_active_mailings_user(owner_id):
        mailing = Mailing.objects.filter(owner=owner_id, is_active=True)

        return mailing.count() if mailing.exists() else 0

    @staticmethod
    def calculate_active_mailings():
        mailing = Mailing.objects.filter(is_active=True)

        return mailing.count() if mailing.exists() else 0


class MailingStatServices:

    @staticmethod
    def all_mailing(owner_id):
        mailing = WorkMailing.objects.filter(owner=owner_id)

        if not mailing.exists():
            return None

        return mailing
