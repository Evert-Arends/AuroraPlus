import os
from AuroraPlus.models import *
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aurora.settings")
django.setup()


class MessagesHandler:
    def __init__(self):
        pass

    @staticmethod
    def get_messages():
        all_messages = Messages.objects.all()
        print all_messages
        return all_messages
