# coding:utf-8
from django import views
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

import DUSite.views
import RedAnt.personalAccount.views
from . import settings

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'DUSite.views.home', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/', admin.site.urls),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
    url(r'^index/', include('RedAnt.index.urls')),
    url(r'^teams/', include('RedAnt.teams.urls')),
    url(r'^courses/', include('RedAnt.courses.urls')),
    url(r'^manage/', include('RedAnt.userManage.urls')),
    url(r'^myaccount/', include('RedAnt.personalAccount.urls')),
    url(r'^forum/',include('RedAnt.forum.urls')),
    url(r'^media/(?P<path>.*)', views.static.serve, {'document_root': settings.MEDIA_ROOT }),
    url(r'^static/(?P<path>.*)', views.static.serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^(?P<path>.*)', views.static.serve, {'document_root': settings.STATIC_ROOT}),

]


