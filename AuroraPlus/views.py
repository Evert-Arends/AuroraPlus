# imports
from array import array

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import get_template
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_protect

from bin import cpu, jsondata, collector
from django.shortcuts import render_to_response, render, redirect
from AuroraPlus.forms import UserForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from models import LandingPageImages

# classes
CPU = cpu.CPUUsage
JsonAction = jsondata.JsonData
Communication = collector.Communication


@login_required
def index(request):
    string_server = JsonAction.all_server_data()
    if not string_server:
        return "No data found"
    count_servers = JsonAction.count_servers()
    if not count_servers:
        return "-"
    return render_to_response('index.html', {'server_all': string_server, 'totalservers': count_servers})


@login_required
def server_page(request, server_id):
    string_server = JsonAction.all_server_data()
    if not string_server:
        return "No data found"
    data_array = CPU.cpu_chart(server_id)
    if not data_array:
        return "0.00,0.00,0.00"
    return render_to_response('server.html', {'server_id': server_id, 'server_all': string_server,
                                              'chart_data': data_array})


def test(request):
    images = LandingPageImages.objects.all().order_by('ID')
    img_array = []
    for image in images:
        img_array.append(image.ID)
        img_array.append(image.PictureLink)
        img_array.append(image.DescText)

    print img_array
    return render_to_response('test.html', {'images': img_array})


def landing_page(request):
    context = RequestContext(request)
    images = LandingPageImages.objects.all().order_by('ID')
    img_array = []
    for image in images:
        img_array.append([image.ID, image.PictureLink, image.DescText])

    print img_array
    return render_to_response('base.html', {'images': img_array}, context)


def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors

    else:
        user_form = UserForm()

    return render(request, 'register.html', {'user_form': user_form, 'registered': registered}, context)


@csrf_protect
def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')

    if request.method == 'POST':
        if request.user.is_authenticated():
            return HttpResponse('You are already logged in.')
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/dashboard/')
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html')


def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
    else:
        return render(request, 'login.html')
    return render(request, 'logout.html')
