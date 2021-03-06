import os
from AuroraPlus.models import *
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aurora.settings")
django.setup()


class MessagesHandler:
    def __init__(self):
        pass

    @staticmethod
    def get_messages(user_id):
        all_messages = Messages.objects.filter(User_ID=user_id).all()

        return all_messages

    @staticmethod
    def count_messages(user_id):
        if user_id is None:
            return 'No messages found.'
        else:
            messages_to_count = Messages.objects.filter(User_ID=user_id, Message_Read=0).count()
            return messages_to_count

    @staticmethod
    def select_message(user_id, message_id):
        selected_message = Messages.objects.filter(User_ID=user_id, ID=message_id).all()

        return selected_message

    @staticmethod
    def message_read(user_id, message_id):
        if user_id is None or message_id is None:
            return 'There has been an error.'
        else:
            try:
                message_to_edit = Messages.objects.get(User_ID=user_id, ID=message_id)
                message_to_edit.Message_Read = 1
                message_to_edit.save()
            except:
                return 'There has been an error(2).'
            return True

    @staticmethod
    def receive_mails(user_id, server_id, checkboxvalue):
        if user_id is None or server_id is None or checkboxvalue is None:
            return 'There has been an error(3).'
        else:
            try:
                receive_mail = Servers.objects.get(User_ID=user_id, ID=server_id)
                receive_mail.Receive_Mail = checkboxvalue
                receive_mail.save()
            except:
                return 'There has been an error(4).'
            return "Success"

    @staticmethod
    def get_mail_state(user_id, server_id):
        if user_id is None or server_id is None:
            return 'There has been an error(5).'
        else:
            mail_state = Servers.objects.get(User_ID=user_id, ID=server_id)

            return mail_state.Receive_Mail
