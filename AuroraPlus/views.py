# Imports
import json
import datetime
import requests
import thread


# Django imports
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

# Application imports
from AuroraPlus.forms import UserForm, OptionsForm

# Local imports
from bin import cpu, jsondata
from bin.ServerManaging import manage, server_edit, server_delete
from bin.ServerMonitoring import collector, count_servers, opacity
from models import LandingPageImages
from bin.ServerMonitoring import monitor, messages, checkbox, collector

# Classes
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
GetLogs = collector.Communication


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

    server_list = Monitor.get_servers(user_id)
    if not server_list:
        return HttpResponse("No servers")

    server_count = str(CountUserServers.count_servers(user_id))

    count_messages = GetMessages.count_messages(user_id)
    if 'Delete' in request.POST.values():
        id = request.POST['id']

    count = User.objects.filter(last_login__startswith=timezone.now().date()).count()

    render_index = {'server_list': server_list, 'server_count': server_count, 'user_count': count,
                    'message_count': count_messages}

    return render(request, 'index.html', render_index)


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
        return render(request, 'edit_server.html', {'Edit_Server_Message': 'No data found.'})

    render_edit_page = {'serverdata': load_server_to_edit}

    return render(request, 'edit_server.html', render_edit_page)


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
        return render(request, 'delete_server.html', {'Delete_Server_Message': 'No data found.'})
    return render(request, 'delete_server.html', {'serverdata': load_server_to_edit})


@login_required
def server_page(request, server_id):
    current_user = request.user
    user_id = current_user.id
    string_server = RetrieveData.all_server_data()
    if string_server is not None:
        valid_json_check = is_json(string_server)
        if not valid_json_check:
            return render(request, 'error.html', {'Error_Message': ['There seems to be no useful json data']})
        else:
            json_obj = json.loads(string_server)
            print json_obj
    else:
        render_error_msg = {'Error_Message': ['There seems to be no useful json data',
                                              'To fix this problem start your client']}
        return render(request, 'error.html', render_error_msg)
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

    server_list = Monitor.get_servers(user_id)
    if not server_list:
        return HttpResponse("No servers.")

    if ram_usage >= 90:
        too_high = 1
    else:
        too_high = 0

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

            GetMessages.receive_mails(user_id, server_id, checkboxvalue)
            Opacity.edit_opacity(user_id, server_id, opacity)

    panel_opacity = Opacity.get_opacity(user_id, server_id)

    render_server_page = {'server_all': string_server, 'chart_data': cpu_average, 'network_sent': network_sent,
                          'network_received': network_received, 'server_name': server_name,
                          'server_list': server_list, 'ssl': server_ssl, 'lan_ip': lan_ip,
                          'disk_usage': disk_usage, 'disk_read': disk_usage_read, 'disk_write': disk_usage_write,
                          'ram_height': too_high, 'cpu_height': cpu_high, 'fillCheckBox': fillcheckbox,
                          'Opacity': panel_opacity, 'opacitystate': opacitystate}

    return render(request, 'server.html', render_server_page)


def live_server_updates(request, chart='CPU_Usage', key='Lqdie4ARBhbJtawrmTBCkenmhb9rvqgRzWN', time=0):
    string_server = RetrieveData.all_server_data()
    if string_server is not None:
        valid_json_check = is_json(string_server)
        if not valid_json_check:
            return render(request, 'error.html', {'Error_Message': ['There seems to be no useful json data']})
        else:
            json_obj = json.loads(string_server)
    else:
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
        json.loads(my_json)
    except ValueError, e:
        return False
    return True


def test(request):
    return HttpResponse('test')


@csrf_protect
def landing_page(request):
    context = RequestContext(request)
    images = LandingPageImages.objects.all().order_by('ID')
    img_array = []

    for image in images:
        img_array.append([image.ID, image.PictureLink, image.DescText])

    render_landingpage = {'images': img_array}
    return render(request, 'base.html', render_landingpage, context)


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

    render_register = {'user_form': user_form, 'registered': registered}

    return render(request, 'register.html', render_register, context)


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

    render_error = {'Error_Message': something_is_wrong}

    return render(request, 'error.html', render_error)


def messages(request, message_id):
    current_user = request.user
    user_id = current_user.id

    all_messages = GetMessages.get_messages(user_id)

    select_message = GetMessages.select_message(user_id, message_id)

    GetMessages.message_read(user_id, message_id)

    render_messages = {'Messages': all_messages, 'selected_message': select_message, 'message_id': message_id}

    return render(request, 'messages.html', render_messages)


def logs(request):
    def getlogs():
        all_logs = GetLogs.get_json_data(time=3600)
        json_data = json.loads(all_logs)
        a = []
        for item in json_data:
            user_logs = item
            user_logs = json.loads(user_logs)

            append_log = user_logs['Server']['Messages']['Log']
            a.append(append_log)

        render_log = {'logs': a}
        return render_log

    thread.start_new_thread(getlogs, ())

    return render(request, 'logs.html', getlogs())

