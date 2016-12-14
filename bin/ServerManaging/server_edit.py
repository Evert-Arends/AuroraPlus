import os
from AuroraPlus.models import *
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aurora.settings")
django.setup()


class EditServer:
    def __init__(self):
        pass

    @staticmethod
    def get_servers(user_id, list_id):
        load_server = Servers.objects.filter(User_ID=user_id, ID=list_id)
        if not load_server:
            return
        print load_server
        return load_server

    @staticmethod
    def edit_server(user_id, list_id, name, description):
        print name, description
        if user_id is None or list_id is None or name is None or description is None:
            return 'Not all variables are fulfilled.'
        else:
            try:
                edited_data = Servers.objects.get(User_ID=user_id, ID=list_id)
                edited_data.Server_Name = name
                edited_data.Server_Description = description
                edited_data.save()
            except:
                return 'Server could not be updated.'
            return True
