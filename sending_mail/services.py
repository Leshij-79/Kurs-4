from sending_mail.models import Messages


class MessagesServices:

    @staticmethod
    def all_messages(owner_id):
        messages = Messages.objects.filter(owner=owner_id)

        if not messages.exists():
            return None

        return messages