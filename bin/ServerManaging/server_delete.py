import os
from AuroraPlus.models import *
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aurora.settings")
django.setup()


class DeleteServer:
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
    def delete_server(user_id, list_id):
        print user_id, list_id
        if user_id is None or list_id is None:
            return 'Entry cannot be deleted.'
        else:
            try:
                server_to_delete = Servers.objects.get(User_ID=user_id, ID=list_id)
                if server_to_delete is not None:
                    server_to_delete.delete()
                else:
                    return 'Entry cannot be deleted.'
            except:
                return 'Entry cannot be deleted.'
            return True
