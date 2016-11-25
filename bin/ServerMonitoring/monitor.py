import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aurora.settings")
django.setup()
from AuroraPlus.models import *


class GetServerData:
    def __init__(self):
        pass

    @staticmethod
    def get_servers(user_id):
        user_servers = Servers.objects.filter(User_ID=user_id)
        if not user_servers:
            return
        return user_servers


if __name__ == "__main__":
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    G = GetServerData.get_servers(1)
    for item in G:
        print item.ID

