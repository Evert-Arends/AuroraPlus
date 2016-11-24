from AuroraPlus.models import Servers


class ManageServer:
    def __init__(self):
        pass

    @staticmethod
    def add_server(name, key, address):
        if not name or key or address:
            print ('Incomplete!')
            name='Berm\'s Server'
            key='fghsdfhfHHJKFGFH677687'
            address='127.0.0.1'


if __name__ == '__main__':
    add_server = ManageServer()
