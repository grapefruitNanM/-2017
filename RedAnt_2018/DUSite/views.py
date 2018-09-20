from django import views
from django.http import HttpResponseRedirect
import urllib.parse


def get_media(request, path):
    url = "/Media/" + path
    return HttpResponseRedirect(url)


def get_static(request, path):
    url = "/Static/" + path
    return HttpResponseRedirect(url)
