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
            data = json.loads(json_string)
            return data
        except:
            return

    @staticmethod
    def count_servers():
        try:
            data = JsonData.get_json_data()
            count = str(len(data['ServerList']['Servers']))
            return count
        except:
            return

    @staticmethod
    def all_server_data():
        try:
            data = JsonData.get_json_data()
            return data['ServerList']['Servers']
        except:
            return
