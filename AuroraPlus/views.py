# imports
import json

import datetime
import time
import requests

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from AuroraPlus.forms import UserForm, OptionsForm

# Local imports
from bin import cpu, jsondata
from bin.ServerManaging import manage, server_edit, server_delete
from bin.ServerMonitoring import collector, count_servers, opacity
from models import LandingPageImages
from bin.ServerMonitoring import monitor, messages, checkbox

# classes
CPU = cpu.CPUUsage
RetrieveData = jsondata.JsonData
Communication = collector.Communication
ServerManager = manage.ManageServer
Monitor = monitor.GetServerData()
EditServers = server_edit.EditServer
DeleteServers = server_delete.DeleteServer
CountUserServers = count_servers.CountServers
GetMessages = messages.MessagesHandler
CheckBoxHandler = checkbox.CheckboxHandler
Opacity = opacity.OpacityHandler


@login_required
@csrf_protect
def index(request):
    # add server form
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
    server_list = Monitor.get_servers(user_id)
    if not server_list:
        return HttpResponse("No servers")

    # counts users servers
    server_count = str(CountUserServers.count_servers(user_id))

    # counting messages
    count_messages = GetMessages.count_messages(user_id)
    # delete server button
    if 'Delete' in request.POST.values():
        id = request.POST['id']

    # count users on account
    count = User.objects.filter(last_login__startswith=timezone.now().date()).count()

    return render(request, 'index.html',
                  {'server_list': server_list, 'server_count': server_count, 'user_count': count,
                   'message_count': count_messages})


@login_required
@csrf_protect
def edit_server(request, list_id):
    current_user = request.user
    user_id = current_user.id

    if request.method == 'POST':
        r = request
        name = r.POST["Name"]
        description = r.POST["Description"]
        if description or name is not None:
            EditServers.edit_server(user_id=user_id, list_id=list_id, name=name, description=description)
        else:
            return render(request, 'edit_server.html', {'Edit_Server_Message': 'ERROR: Fill out all fields.'})
        return render(request, 'edit_server.html', {'Edit_Server_Message': 'Successfully updated.'})

    load_server_to_edit = EditServers.get_servers(user_id, list_id)
    if not load_server_to_edit:
        print user_id, list_id
        return render(request, 'edit_server.html', {'Edit_Server_Message': 'No data found.'})
    print user_id, list_id
    print load_server_to_edit.values('Server_Name', 'Server_key', 'Server_Description')
    return render(request, 'edit_server.html', {'serverdata': load_server_to_edit})


@login_required
@csrf_protect
def delete_server(request, list_id):
    current_user = request.user
    user_id = current_user.id

    if request.method == 'POST':
        DeleteServers.delete_server(user_id=user_id, list_id=list_id)
        return render(request, 'delete_server.html', {'Delete_Server_Message': 'Successfully deleted.'})

    load_server_to_edit = EditServers.get_servers(user_id, list_id)
    if not load_server_to_edit:
        print user_id, list_id
        return render(request, 'delete_server.html', {'Delete_Server_Message': 'No data found.'})
    return render(request, 'delete_server.html', {'serverdata': load_server_to_edit})


@login_required
def server_page(request, server_id):
    current_user = request.user
    user_id = current_user.id
    # For a while we will store the data here, this should be moved to the controller.
    string_server = RetrieveData.all_server_data()
    if string_server is not None:
        valid_json_check = is_json(string_server)
        if not valid_json_check:
            return render(request, 'error.html', {'Error_Message': ['There seems to be no useful json data']})
        else:
            json_obj = json.loads(string_server)
            print json_obj
    else:
        return render(request, 'error.html', {
            'Error_Message': ['There seems to be no useful json data', 'To fix this problem start your client']})
    network_sent = json_obj['Server']['ServerDetails']['NetworkLoad']['Sent']
    network_received = json_obj['Server']['ServerDetails']['NetworkLoad']['Received']
    cpu_average = json_obj["Server"]["ServerDetails"]["CPU_Usage"]
    server_name = json_obj["Server"]["ServerDetails"]["ServerName"]
    server_ssl = json_obj["RequestDetails"]["Connection"]["SSL"]
    lan_ip = json_obj["RequestDetails"]["Connection"]["LAN IPAddress"]
    disk_usage = json_obj["Server"]["ServerDetails"]["Disk_Usage"]
    disk_usage_read = json_obj['Server']['ServerDetails']['Disk_Load']['Read']
    disk_usage_write = json_obj['Server']['ServerDetails']['Disk_Load']['Write']
    ram_usage = json_obj["Server"]["ServerDetails"]["Ram_Usage"]

    if not network_sent:
        network_sent = '0'

    # Get all the users servers.
    server_list = Monitor.get_servers(user_id)
    if not server_list:
        return HttpResponse("No servers.")

    # check height RAM usage
    if ram_usage >= 90:
        too_high = 1
    else:
        too_high = 0

    # check cpu height
    if cpu_average >= 90:
        cpu_high = 1
    else:
        cpu_high = 0

    getmailstate = GetMessages.get_mail_state(user_id, server_id)
    fillcheckbox = ""
    if getmailstate == 1:
        fillcheckbox = "checked"

    getopacitystate = Opacity.get_opacity(user_id, server_id)
    opacitystate = ""
    if getopacitystate == 1:
        opacitystate = "checked"

    form = OptionsForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            checkboxvalue = request.POST.get("active_monitoring", False)

            opacity = request.POST.get("opacity", False)

            receive_error_mails = GetMessages.receive_mails(user_id, server_id, checkboxvalue)
            set_opacity = Opacity.edit_opacity(user_id, server_id, opacity)

    panel_opacity = Opacity.get_opacity(user_id, server_id)

    return render(request, 'server.html', {'server_all': string_server,
                                           'chart_data': cpu_average, 'network_sent': network_sent,
                                           'network_received': network_received, 'server_name': server_name,
                                           'server_list': server_list, 'ssl': server_ssl, 'lan_ip': lan_ip,
                                           'disk_usage': disk_usage, 'disk_read': disk_usage_read,
                                           'disk_write': disk_usage_write, 'ram_height': too_high,
                                           'cpu_height': cpu_high, 'fillCheckBox': fillcheckbox,
                                           'Opacity': panel_opacity, 'opacitystate': opacitystate})


def live_server_updates(request, chart='CPU_Usage', key='Lqdie4ARBhbJtawrmTBCkenmhb9rvqgRzWN', time=0):
    string_server = RetrieveData.all_server_data()
    if string_server is not None:
        valid_json_check = is_json(string_server)
        if not valid_json_check:
            return render(request, 'error.html', {'Error_Message': ['There seems to be no useful json data']})
        else:
            json_obj = json.loads(string_server)
    else:
        # test
        return render(request, 'error.html', {
            'Error_Message': ['There seems to be no useful json data', 'To fix this problem start your client']})
    return_json_obj = {'Sent': '0', 'Received': '0'}
    if chart == 'CPU_Usage':
        usage = json_obj["Server"]["ServerDetails"]["CPU_Usage"]
    elif chart == 'Network_Usage':
        sent = json_obj['Server']['ServerDetails']['NetworkLoad']['Sent']
        received = json_obj['Server']['ServerDetails']['NetworkLoad']['Received']
        return_json_obj['Sent'] = sent
        return_json_obj['Received'] = received

        usage = json.dumps(return_json_obj)
    elif chart == 'ping':
        r = requests.get('http://127.0.0.1:8001')
        if r.status_code == 200:
            ping = r.elapsed.total_seconds()
            ping *= 1000
        else:
            ping = 2
        usage = ping

    elif chart == 'RAM_Usage':
        usage = json_obj["Server"]["ServerDetails"]["Ram_Usage"]
        if not usage:
            usage = 0
    elif chart == 'Online':
        old_date = json_obj["RequestDetails"]["Time"]["RequestSent"]
        if not old_date:
            usage = False
        old_date = float(old_date)
        old_date = datetime.datetime.fromtimestamp(old_date)
        if old_date < datetime.datetime.now()-datetime.timedelta(seconds=2.5):
            usage = 'Server is offline!'
        else:
            usage = 'Server is online!'
    else:
        usage = 'Failed'
        return HttpResponse(usage, status=400)
    return HttpResponse(usage, status=200)


def is_json(my_json):
    try:
        json_object = json.loads(my_json)
    except ValueError, e:
        return False
    return True


def test(request):
    # return render(request, 'server_page_properties/ping.html')
    return HttpResponse('test')


@csrf_protect
def landing_page(request):
    context = RequestContext(request)
    images = LandingPageImages.objects.all().order_by('ID')
    img_array = []
    for image in images:
        img_array.append([image.ID, image.PictureLink, image.DescText])

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


def error(request):
    something_is_wrong = ['Have you tried turning it off and on again?']
    return render(request, 'error.html', {'Error_Message': something_is_wrong})


def messages(request, message_id):
    # get user_id
    current_user = request.user
    user_id = current_user.id

    # get messages on user_id
    all_messages = GetMessages.get_messages(user_id)

    # select message from menu
    select_message = GetMessages.select_message(user_id, message_id)

    # update messages from unread to read
    message_read = GetMessages.message_read(user_id, message_id)
    return render(request, 'messages.html', {'Messages': all_messages, 'selected_message': select_message,
                                             'message_id': message_id})
