# imports
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from bin import cpu, jsondata, collector
from django.shortcuts import render_to_response
from AuroraPlus.forms import UserForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from models import LandingPageImages


# classes
CPU = cpu.CPUUsage
JsonAction = jsondata.JsonData
Communication = collector.Communication


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


def test(request):
    image = LandingPageImages(
        PictureLinkName="image1",
        PictureLink="http://imgur.com/Sdy6Vq0.png",
        DescText="Clean overview of all your servers and all the necessary data you need. "
                 "We designed it to be clean, understandable and modern looking."
    )

    image.save()

    image2 = LandingPageImages(
        PictureLinkName="image2",
        PictureLink="http://imgur.com/VgE7yXo.png",
        DescText="In the dashboard menu you can choose the server you want to see. "
                 "In this case server 1, server 2 en server 3."
    )

    image2.save()

    image3 = LandingPageImages(
        PictureLinkName="image3",
        PictureLink="http://imgur.com/qIxUbVi.png",
        DescText="Once on the server page, the details are displayed in the graphics. "
                 "Monitoring your servers was never this easy!"
    )

    image3.save()
    return render_to_response('test.html')


def landing_page(request):
    images_object = LandingPageImages
    print images_object
    context = RequestContext(request)
    return render_to_response('base.html', context)


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

    return render_to_response('register.html', {'user_form': user_form, 'registered': registered}, context)


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/base/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render_to_response('login.html', {}, context)


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/base/')
