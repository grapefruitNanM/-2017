#coding:utf-8
from RedAnt.forms import teamForm,myUEditorModelForm,FileUploadForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from RedAnt.models import ProjectTeam,Blog,LearningResources,inviteCode,Course,log
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
import DUSite
from bs4 import BeautifulSoup
from DUSite import settings
import urllib.request
import json
import re
import datetime
import random

@login_required
def manage(request):
    if request.method == 'POST':
        userlist = request.POST.get("userList")
        status = request.POST.get("status")
        try:
            names = re.findall(r"'username':'(.+?)'", userlist)
            if status == 'changeRank':
                for username in names:
                    user = User.objects.get(username=username)
                    group = Group.objects.get(name='user')
                    user.groups.remove(group)
                    group = Group.objects.get(name='admin')
                    user.groups.add(group)
                data = {'code': '1', 'info': u'修改成功'}
            else:
                for username in names:
                    User.objects.get(username=username).delete()
                data = {'code': '1', 'info': u'删除成功'}
            return JsonResponse(data)
        except:
            data = {'code': '0', 'info': u'修改失败'}
            return JsonResponse(data)
    else:
        users = User.objects.filter(groups__name='user')
        teams = ProjectTeam.objects.all()
        courses = Course.objects.all()
        return render(request, 'manager.html',{'users':users, 'teams': teams,'courses': courses})

@login_required
def vip_manage(request):
    if request.method == 'POST':
        userlist = request.POST.get("userList")
        status = request.POST.get("status")
        names = re.findall(r"'username':'(.+?)'", userlist)
        try:
            if status == 'changeRank':
                for username in names:
                    user = User.objects.get(username=username)
                    group = Group.objects.get(name='admin')
                    user.groups.remove(group)
                    group = Group.objects.get(name='user')
                    user.groups.add(group)
                data = {'code': '1', 'info': u'修改成功'}
            else:
                for username in names:
                    User.objects.get(username=username).delete()
                data = {'code': '1', 'info': u'删除成功'}
            return JsonResponse(data)
        except:
            data = {'code': '0', 'info': u'修改失败'}
            return JsonResponse(data)
    else:
        users = User.objects.filter(groups__name='admin')
        teams = ProjectTeam.objects.all()
        courses = Course.objects.all()
        return render(request, 'powerUserManage.html',{'users':users, 'teams': teams,'courses': courses})

@login_required
def invitation(request):
    if request.method == 'POST':
        code = request.POST.get("invitation")
        time = request.POST.get("time")
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        if(now>time):
            data = {'code': '0', 'info': u'时间无效'}
            return JsonResponse(data)
        inviteCode.objects.all().delete()
        invitation = inviteCode(code = code,ddl = time)
        invitation.save()
        data = {'code': '1', 'info': u'修改成功'}
        return JsonResponse(data)
    else:
        teams = ProjectTeam.objects.all()
        invitation = inviteCode.objects.get()
        courses = Course.objects.all()
        return render(request,'invitation.html',{'teams': teams,'inviteCode':invitation,'courses': courses})

@login_required
def changeGroup(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        team = request.POST.get("team")
        try:
            user = User.objects.get(email =email)
            user.first_name = team
            user.save()
            data = {'code': '1', 'info': u'修改成功'}
            return JsonResponse(data)
        except:
            data = {'code': '0', 'info': u'用户不存在'}
            return JsonResponse(data)

@login_required
def userLog(request):
    teams = ProjectTeam.objects.all()
    courses = Course.objects.all()
    logs = log.objects.all()
    return render(request, 'userLogs.html', {'teams': teams, 'courses': courses,'logs':logs})

@login_required
def emailManage(request):
    teams = ProjectTeam.objects.all()
    courses = Course.objects.all()
    f = open(settings.STATIC_ROOT + "/email", "r")  # 打开文件
    host = f.readline().rstrip('\n')  # 读一行
    email = f.readline().rstrip('\n')  # 读一行
    f.close()
    return render(request, 'changeMail.html', {'teams': teams, 'courses': courses,'email':email})

@login_required
def changEmail(request):
    if request.method == 'POST':
        mail = request.POST.get("mail")
        code = request.POST.get("code")
        format = re.findall(r"@(.+?)\.", mail)
        if re.findall(r"@(.+?)\.", mail):
            f = open(settings.STATIC_ROOT + "email", "w")  # 打开文件
            if format[0] == '163' or format[0] == 'qq':
                if format[0] == '163':
                    seq = ['smtp.163.com\n', mail+'\n', code+'\n']
                if format[0] == 'qq':
                    seq = ['smtp.qq.com\n', mail + '\n', code + '\n']
                f.writelines(seq)
                data = {'code': '1', 'info': u'修改成功'}
                f.close()
                return JsonResponse(data)
