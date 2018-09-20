
from django.conf.urls import include, url
import RedAnt.file.views as views

urlpatterns = [
    url(r'', views.getFile),
]