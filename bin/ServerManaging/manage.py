import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aurora.settings")
django.setup()
from AuroraPlus.models import *


class ManageServer:
    def __init__(self):
        pass

    @staticmethod
    def add_server(name, key, address, description, user_id):
        print name, key, address
        if name is None or key is None or address is None or user_id is None:
            return 'Not all variables are fulfilled.'
        else:
            new_server_entry = Servers(User_ID=user_id, Server_Name=name, Server_key=key,
                                       Server_Description=description)
            new_server_entry.save()
            return True

if __name__ == '__main__':
    add_server = ManageServer()
