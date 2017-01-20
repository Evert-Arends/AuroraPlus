# Define server variables here.

DEBUG = False

if DEBUG:
    API_SERVER_PROTOCOL = 'http://'  # Change this to https when you switch to SSL.
    API_SERVER_BASE = '127.0.0.1'
    API_SERVER_PORT = '8001'
    API_CLIENT_URL = '/client_details/'
else:
    API_SERVER_PROTOCOL = 'http://'  # Change this to https when you switch to SSL.
    API_SERVER_BASE = '51.15.63.248'
    API_SERVER_PORT = '80'
    API_CLIENT_URL = '/client_details/'


# Do not touch zone.
API_SERVER_ADDRESS = '{0}:{2}'.format(API_SERVER_BASE, ':', API_SERVER_PORT)


