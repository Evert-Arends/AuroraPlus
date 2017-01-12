import os
from AuroraPlus.models import *
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aurora.settings")
django.setup()


class OpacityHandler:
    def __init__(self):
        pass

    @staticmethod
    def get_opacity(user_id, server_id):
        opacity = Servers.objects.get(User_ID=user_id, ID=server_id)

        return opacity.Server_Opacity

    @staticmethod
    def edit_opacity(user_id, server_id, opacity):
        print user_id, opacity
        if user_id is None or opacity is None or server_id is None:
            return 'There has been an error(3).'
        else:
            try:
                update_opacity = Servers.objects.get(User_ID=user_id, ID=server_id)
                update_opacity.Server_Opacity = opacity
                update_opacity.save()
            except:
                return 'There has been an error(4).'
            return "Success"
