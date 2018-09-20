
from django.conf.urls import include, url
import RedAnt.courses.views as views

urlpatterns = [
    url(r'major=(?P<name>.*)/edit/', views.courseEdit),
    url(r'major=(?P<name>.*)/', views.courseMajor),
    url(r'major=(?P<name>.*)', views.courseMajor),
    url(r'operating=new/', views.courseAdd),
    url(r'zj_del', views.zhangjie_del),
    url(r'zhangjie_small_add', views.zhangjie_small_add),
    url(r'zhangjie_add', views.zhangjie_add),
    ]