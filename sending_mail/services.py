from sending_mail.models import Messages, Recipients


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
