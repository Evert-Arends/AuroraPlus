from django.shortcuts import render, render_to_response
import json



# Create your views here.
from django.template import RequestContext


with open('./testing/data.json') as data_file:
    data = json.load(data_file)
    print data


def index(request):
    decoded_json = data
    return render_to_response('index.html', {'results': decoded_json}, SetVarNode)
