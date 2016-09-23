from django.shortcuts import render, render_to_response
import json

from django.contrib.auth.models import User
import arrow

from django.views.generic import TemplateView

# Create your views here.
from django.template import RequestContext


with open('./testing/names.json') as names_file:
    names = json.load(names_file)
    print names

with open('./testing/data.json') as data_file:
    data = json.load(data_file)
    print data


def index(request):
    decoded_data = data
    decoded_names = names
    return render_to_response('index.html', {'server_names': decoded_names, 'server_data': decoded_data})


def server_page(request, id):
    decoded_data = data
    decoded_names = names
    req = id
    print req
    return render_to_response('server.html', {'server_names': decoded_names, 'server_data': decoded_data, 'id': req})


def test(request):
    return render_to_response('test.html')

