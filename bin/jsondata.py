import json

from bin.ServerMonitoring import collector


# classes
Communication = collector.Communication


class JsonData:

    def __init__(self):
        return

    @staticmethod
    def get_json_data():
        try:
            json_string = Communication.get_json_data()
            print json_string
            return json_string
        except:
            return

    @staticmethod
    def count_servers():
        try:
            data = JsonData.get_json_data()
            count = data
            return count
        except:
            return

    @staticmethod
    def all_server_data():
        try:
            data = JsonData.get_json_data()
            return data
        except:
            return

if __name__ == '__main__':
    c = JsonData()
    d = c.count_servers()


