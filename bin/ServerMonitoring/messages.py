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
        print all_messages

        for item in all_messages:
            print item.ID, item.Date_Received

        return all_messages

    @staticmethod
    def count_messages(user_id):
        print user_id
        if user_id is None:
            return 'No messages found.'
        else:
            messages_to_count = Messages.objects.filter(User_ID=user_id).count()
            print messages_to_count
            return messages_to_count

    @staticmethod
    def select_message(user_id, message_id):
        selected_message = Messages.objects.filter(User_ID=user_id, ID=message_id).all()
        print selected_message

        for item in selected_message:
            print item.ID, item.Date_Received

        return selected_message

    @staticmethod
    def message_read(user_id, message_id):
        print user_id, message_id
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
