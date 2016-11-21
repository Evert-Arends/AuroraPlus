import json

import requests
from AuroraPlus.settings import constants


class Communication:
    def __init__(self):
        print ('Collecting!')

    def retrieve_data(self):
        pass

    # There still must be a time backwards
    # the parameters have a default value, for testing, if you assign this method with different parameters
    # those standard values will be overwritten.
    @staticmethod
    def get_json_data(server='Lqdie4ARBhbJtawrmTBCkenmhb9rvqgRzWN', time=0):
        api = constants.API_SERVER_ADDRESS
        client_address = constants.API_CLIENT_URL
        if time != 0:
            ## WORKING ON THIS!!
            url = '{0}{1}{2}{3}/time/{4}'.format(constants.API_SERVER_ADDRESS, api, client_address, server, time)
            # url = (constants.API_SERVER_PROTOCOL + api + client_address + server + '')
        else:
            url = (constants.API_SERVER_PROTOCOL + api + client_address + server)

        request = requests.get(url)
        if request.status_code != 200:
            print 'Something wrong with your api? Seems like I cannot connect.'
            return

        raw_json_content = request.content
        if raw_json_content:
            purified_json_content = json.loads(raw_json_content)
            return purified_json_content
        else:
            return

if __name__ == "__main__":
    Collector = Communication()
    print Collector.get_json_data()
