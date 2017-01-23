import json

from bin.ServerMonitoring import collector


# classes
Communication = collector.Communication


class JsonData:

    def __init__(self):
        return

    @staticmethod
    def get_json_data(server):
        try:
            json_string = Communication.get_json_data(server=server)
            print json_string
            return json_string
        except:
            return

    @staticmethod
    def count_servers(server='Lqdie4ARBhbJtawrmTBCkenmhb9rvqgRzWN'):
        try:
            data = JsonData.get_json_data(server=server)
            count = data
            return count
        except:
            return

    @staticmethod
    def all_server_data(server='Lqdie4ARBhbJtawrmTBCkenmhb9rvqgRzWN'):
        try:
            data = JsonData.get_json_data(server=server)
            return data
        except:
            return

if __name__ == '__main__':
    c = JsonData()
    d = c.count_servers()


