import requests
from AuroraPlus.settings import constants


class Communication:
    def __init__(self):
        print ('Collecting!')

    def retrieve_data(self):
        pass

    # There still must be a time backwards
    # the parameters have a default value, for testing, if you assign this method with different parmeters
    # those standard values will be overwritten.
    @staticmethod
    def get_json_data(server='Lqdie4ARBhbJtawrmTBCkenmhb9rvqgRzWN', time=0):
        api = constants.API_SERVER_ADDRESS
        client_address = constants.API_CLIENT_URL
        url = (constants.API_SERVER_PROTOCOL + api + client_address + server)

        json_data = requests.get(url)
        if json_data.status_code != 200:
            print 'Something wrong with your api? Seems like I cannot connect.'
            return

        json = json_data.content
        if json:
            return json
        else:
            return

if __name__ == "__main__":
    Collector = Communication()
    print Collector.get_json_data()





