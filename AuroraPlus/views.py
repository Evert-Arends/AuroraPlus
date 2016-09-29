from django.shortcuts import render, render_to_response
import json

import array
from pprint import pprint

from django.views.generic import TemplateView

# Create your views here.
from django.template import RequestContext

with open('./testing/data.json', 'r') as f:
    json_data = json.load(f)
    string_server = json_data['ServerList']['Servers']

with open('./testing/data.json') as data_file:
    data = json.load(data_file)
    count = str(len(data['ServerList']['Servers']))
    print count


def getServer(server_id):
    server_id = int(server_id)
    cpu_usage = (data["ServerList"]["Servers"][server_id]["ServerData"]["Cpu"])

    if not cpu_usage:
        return
    else:
        return cpu_usage


def index(request):
    print string_server
    print count
    return render_to_response('index.html', {'server_all': string_server, 'totalservers': count})


def server_page(request, server_id):
    req = server_id
    print req
    chart_data = getServer(server_id)
    escaped = chart_data.replace(",", ".")
    splitted = escaped.replace(";", ",")
    final = splitted.split(',')
    item1 = float(final[0]) * 100
    item2 = float(final[1]) * 100
    item3 = float(final[2]) * 100
    data_array = [item1, item2, item3]
    print data_array
    return render_to_response('server.html', {'server_id': req, 'server_all': string_server, 'chart_data': data_array})


def test(request):
    return render_to_response('test.html')

