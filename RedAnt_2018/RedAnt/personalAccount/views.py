#coding:utf-8
from RedAnt.forms import myUEditorModelForm,FileUploadForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from RedAnt.models import Blog,ProjectTeam,Photo,Course
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
import DUSite
from bs4 import BeautifulSoup
import urllib.request
import json
import re
import datetime
import random


@login_required
def account_manager(request):
    if request.method == 'POST':
        username = request.POST.get("username", False)
        email = request.POST.get("email", False)
        prePsw = request.POST.get("prePassword", False)
        password = request.POST.get("password", False)
        try:
            user = User.objects.get(username=username)
            if(request.user == user):
                raise
            data = {'code': '0', 'info': u'用户名冲突'}
            return JsonResponse(data)
        except:
            try:
                user = User.objects.get(email=email)
                if (request.user == user):
                    raise
                data = {'code': '0', 'info': u'邮箱已注册'}
                return JsonResponse(data)
            except User.DoesNotExist:
                if(username.strip() !=''):
                    request.user.username = username
                if (email.strip() != ''):
                    request.user.email = email
                if (password.strip() != '' and prePsw.strip() != ''):
                    user = request.user
                    username = user.username
                    user = authenticate(username=username, password=prePsw)
                    if user is not None:
                        request.user.set_password(password)
                    else:
                        data = {'code': '0', 'info': u'旧密码错误'}
                        return JsonResponse(data)
                    request.user.set_password(password)
                request.user.save()
                data = {'code': '1', 'info': u'保存成功'}
                return JsonResponse(data)
    else:
        teams = ProjectTeam.objects.all()
        fileForm = FileUploadForm()
        courses = Course.objects.all()
        return render(request, 'personalCenter.html', {'teams': teams,'fileForm': fileForm,'courses': courses})

@login_required
def checkPrepsw(request):
    if request.method == 'POST':
        prePsw = request.POST.get("oldPsw", False)
        user = request.user
        username = user.username
        # 获取的表单数据与数据库进行比较
        user = authenticate(username=username, password=prePsw)
        if user is not None:
            data = {'code': '1', 'info': u'验证成功'}
        else:
            data = {'code': '0', 'info': u'密码错误'}
        return JsonResponse(data)


@login_required
def accountImgChange(request):
    if request.method == 'POST':
        fileForm = FileUploadForm(request.POST, request.FILES)
        if fileForm.is_valid():
            photo = Photo()
            photo.fileField = fileForm.cleaned_data['file']
            photo.save()
            try:
                Photo.objects.get(fileField = request.user.last_name).delete()
                request.user.last_name = photo.fileField
                request.user.save()
                url = '/myaccount/'
                return HttpResponseRedirect(url)
            except:
                request.user.last_name = photo.fileField
                request.user.save()
                url = '/myaccount/'
                return HttpResponseRedirect(url)