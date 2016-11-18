import json

class JsonData:

    def __init__(self):
        return

    @staticmethod
    def get_json_data():
        try:
            data = json.loads(open('./testing/data.json').read())
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
