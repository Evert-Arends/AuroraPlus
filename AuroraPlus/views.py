# imports
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from AuroraPlus.forms import UserForm

# Local imports
from bin import cpu, jsondata
from bin.ServerManaging import manage
from bin.ServerMonitoring import collector
from models import LandingPageImages
from bin.ServerMonitoring import monitor

# classes
CPU = cpu.CPUUsage
JsonAction = jsondata.JsonData
Communication = collector.Communication
ServerManager = manage.ManageServer
Monitor = monitor.GetServerData()


@login_required
@csrf_protect
def index(request):
    current_user = request.user
    user_id = current_user.id
    if request.method == 'POST':
        r = request
        name = r.POST["Name"]
        key = r.POST["Key"]
        description = r.POST["ServerDescription"]
        if description or name or key is not None:
            ServerManager.add_server(name=name, key=key, address='127.0.0.1', user_id=user_id, description=description)
        else:
            return render(request, 'index.html',
                          {'Add_Server_Error': 'Please fill in the whole form, and try to use the accepted character.'})

    # Get all the users servers.
    string_server = Monitor.get_servers(user_id)
    if not string_server:
        print string_server
        return HttpResponse("No data found")

    count_servers = JsonAction.count_servers()
    if not count_servers:
        count_servers = '--'
    return render(request, 'index.html', {'server_all': string_server, 'totalservers': count_servers})


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
    import json
    GetJsonData = Communication.get_json_data()

    j = json.loads(GetJsonData)
    print j
    results = j['Server']['ServerDetails']
    print results
    return render(request, 'test.html', j, results)


@csrf_protect
def landing_page(request):
    context = RequestContext(request)
    images = LandingPageImages.objects.all().order_by('ID')
    img_array = []
    for image in images:
        img_array.append([image.ID, image.PictureLink, image.DescText])

    print img_array
    return render(request, 'base.html', {'images': img_array}, context)


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
            valid_login = False
            return render(request, 'login.html', {'Login': valid_login})
            # return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html', {'Login': 'True'})


def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
    else:
        return render(request, 'login.html')
    return render(request, 'logout.html')


def page_not_found(request):
    return render(request, '404.html')
