import os
from AuroraPlus.models import *
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aurora.settings")
django.setup()


class CountServers:
    def __init__(self):
        pass

    @staticmethod
    def count_servers(user_id):
        print user_id
        if user_id is None:
            return 'No servers found.'
        else:
            servers_to_count = Servers.objects.filter(User_ID=user_id).count()
            print servers_to_count
            return servers_to_count
