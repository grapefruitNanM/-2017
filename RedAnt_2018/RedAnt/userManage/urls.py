from django.conf.urls import include, url
import RedAnt.userManage.views as views

urlpatterns = [
    url(r'changeGroup/', views.changeGroup),
    url(r'log/', views.userLog),
    url(r'invitation/', views.invitation),
    url(r'powerUser/', views.vip_manage),
    url(r'changeMail/', views.emailManage),
    url(r'changeEmail/', views.changEmail),
    url(r'', views.manage),
    ]