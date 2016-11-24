"""Aurora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from AuroraPlus import views


urlpatterns = [
    url(r'^$', views.landing_page, name='landing_page'),
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', views.index, name='index'),
    url(r'^server/(?P<server_id>\w{0,50})$', views.server_page, name='server'),
    url(r'^test/', views.test, name='test'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^add_server/$', views.add_server, name='addserver'),
    url(r'^pagenotfound/$', views.page_not_found, name='pagenotfound'),
]
