from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from bin import cpu, jsondata
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

CPU = cpu.CPUUsage
JsonAction = jsondata.JsonData


def index(request):
    string_server = JsonAction.all_server_data()
    if not string_server:
        return "No data found"
    count_servers = JsonAction.count_servers()
    if not count_servers:
        return "-"
    return render_to_response('index.html', {'server_all': string_server, 'totalservers': count_servers})


def server_page(request, server_id):
    string_server = JsonAction.all_server_data()
    if not string_server:
        return "No data found"
    data_array = CPU.cpu_chart(server_id)
    if not data_array:
        return "0.00,0.00,0.00"
    return render_to_response('server.html', {'server_id': server_id, 'server_all': string_server,
                                              'chart_data': data_array})


@csrf_protect
def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username="test", password="test")

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Aurora+ account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)


@csrf_protect
def test(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")
    # return render_to_response('test.html')
