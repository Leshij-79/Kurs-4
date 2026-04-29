from smtplib import SMTPException

from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from sending_mail.models import Mailing, Messages, Recipients, WorkMailing
from users.models import CustomUser


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

    @staticmethod
    def send_mailing(email_owner, mailing_pk):
        mailing = Mailing.objects.get(pk=mailing_pk)
        owner = CustomUser.objects.get(email=email_owner)
        recipients = mailing.recipients.all()

        for recipient in recipients:
            email_attempt = WorkMailing(mailing=mailing)
            email_attempt.attempt_time = timezone.now()
            email_attempt.owner = owner
            email_attempt.recipient = recipient
            email_attempt.mailing = mailing

            try:
                server_response = send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.mail_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient.email],
                )

                if server_response == 1:
                    email_attempt.status = "success"
                    email_attempt.server_response = "Письмо принято SMTP-сервером"
                else:
                    email_attempt.status = "failed"
                    email_attempt.server_response = "Неизвестная ошибка отправки"

            except SMTPException as e:
                email_attempt.status = "failed"
                email_attempt.server_response = f"Ошибка SMTP: {str(e)}"

            except Exception as e:
                email_attempt.status = "failed"
                email_attempt.server_response = f"Внутренняя ошибка сервера: {str(e)}"

            email_attempt.save()

        return


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


def get_index_cached(cache_key, cache_timeout):
    index = cache.get(cache_key)

    if index is None:
        index = Mailing.objects.all()
        cache.set(cache_key, index, cache_timeout)

    return index


def get_messages_cached(cache_key, cache_timeout):
    messages = cache.get(cache_key)

    if messages is None:
        messages = Mailing.objects.all()
        cache.set(cache_key, messages, cache_timeout)

    return messages
