from django.shortcuts import render, render_to_response


# Create your views here.
from django.template import RequestContext


def index(request):
    server_list = ["server1", "server2", "server3", "server4", ]
    return render_to_response('index.html', {'servers': server_list}, request)