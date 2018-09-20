
from django.conf.urls import include, url
import RedAnt.index.views as views

urlpatterns = [
    url(r'changePoster/delete=(?P<name>.*)/', views.deletePoster),
    url(r'changePoster/', views.changePoster),
    url(r'contactUs/', views.contactUs),
    url(r'introduce/', views.introduce),
    url(r'forget/', views.forget),
    url(r'sign_in/', views.sign_in),
    url(r'sign_up/', views.sign_up),
    url(r'emailSend/', views.emailSend),
    url(r'emailCheck/', views.emailCheck),
    url(r'userCheck/', views.userCheck),
    url(r'logout/', views.logout_system),
    url(r'', views.index),
    ]