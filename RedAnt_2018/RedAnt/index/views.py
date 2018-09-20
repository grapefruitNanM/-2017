# coding:utf-8
from RedAnt.forms import myUEditorModelForm, FileUploadForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from RedAnt.models import Blog, ProjectTeam, inviteCode, Introduction, ContactUs, Poster, Course
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
from django.core.mail import send_mail
from DUSite import settings

import uuid


def random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.upper()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    return random[0:string_length]  # Return the random string.


def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get("email", False)
        password = request.POST.get("password", False)
        print(email, password)
        try:
            user = User.objects.get(email=email)
            username = user.username
            # 获取的表单数据与数据库进行比较
            print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # 登录用户
                data = {'code': '1', 'info': u'登录成功', 'url': 'index'}
            else:
                data = {'code': '0', 'info': u'邮箱或密码错误'}
            return JsonResponse(data)
        except User.DoesNotExist:
            data = {'code': '0', 'info': u'邮箱或密码错误'}
            return JsonResponse(data)
    else:
        teams = ProjectTeam.objects.all()
        for team in teams:
            key = team.Introduction
            soup = BeautifulSoup(key, "html5lib")
            team.Introduction = soup.text[0:100] + '...'
        introduction = Introduction.objects.get()
        contact = ContactUs.objects.get()
        posters = Poster.objects.all()
        courses = Course.objects.all()
        return render(request, 'signIn.html',
                      {'teams': teams, 'introduction': introduction, 'contact': contact, 'posters': posters,
                       'courses': courses})


def forget(request):
    if request.method == 'POST':
        email = request.POST.get("email", False)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            data = {'code': '0', 'info': u'账户不存在'}
            return JsonResponse(data)
        content = random_string(8)
        user.set_password(content)
        user.save()
        subject = '找回密码'
        f = open(settings.STATIC_ROOT + "/email", "r")
        host = f.readline().rstrip('\n')
        form_email = f.readline().rstrip('\n')
        f.close()
        send_mail(
            subject=subject, message=content,
            from_email=form_email, recipient_list=[email, ], fail_silently=False,
        )
        data = {'code': '1', 'info': u'新密码已发到邮箱，注意查收', 'url': 'index'}
        return JsonResponse(data)


def logout_system(request):
    """
    退出登录
    :param request:
    :return:
    """
    logout(request)
    return HttpResponseRedirect('/index/sign_in/')


def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get("username", False)
        email = request.POST.get("email", False)
        password = request.POST['password']
        team = request.POST['project']
        code = request.POST['invitation']
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        if code != inviteCode.objects.get().code or inviteCode.objects.get().ddl < now:
            data = {'code': '0', 'info': u'邀请码无效'}
            return JsonResponse(data)
        try:
            User.objects.get(username=username)
            data = {'code': '0', 'info': u'用户名冲突'}
            return JsonResponse(data)
        except:
            try:
                User.objects.get(email=email)
                data = {'code': '0', 'info': u'邮箱已注册'}
                return JsonResponse(data)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, email=email, password=password)
                if user is not None:
                    user.first_name = team
                    user.last_name = 'photos/23.jpg'
                    group = Group.objects.get(name='user')
                    user.groups.add(group)
                    user.save()
                    login(request, user)
                    data = {'code': '1', 'info': u'注册成功'}
                    return JsonResponse(data)
    else:
        courses = Course.objects.all()
        return render(request, 'signUp.html', {'teams': ProjectTeam.objects.all(), 'courses': courses})


def emailSend(request):
    if request.method == 'POST':
        try:
            senderEmail = request.POST.get("from", False)
            sender = request.POST.get("sender", False)
            content = request.POST.get("content", False)
            msg = sender + '  ' + senderEmail
            f = open(settings.STATIC_ROOT + "/email", "r")  # 打开文件
            host = f.readline().rstrip('\n')  # 读一行
            email = f.readline().rstrip('\n')  # 读一行
            f.close()
            subject, form_email, to = msg, email, email
            text_content = content
            send_mail(
                subject=subject, message=text_content,
                from_email=form_email, recipient_list=[to, ], fail_silently=False,
            )
            data = {'code': '1', 'info': u'邮件发送成功！'}
            return JsonResponse(data)
        except:
            data = {'code': '0', 'info': u'邮件发送失败'}
            return JsonResponse(data)


def emailCheck(request):
    if request.method == 'POST':
        email = request.POST.get("email", False)
        try:
            User.objects.get(email=email)
            data = {'code': '0', 'info': u'邮箱已注册'}
            return JsonResponse(data)
        except:
            data = {'code': '1', 'info': u'邮箱可用'}
            return JsonResponse(data)


def userCheck(request):
    if request.method == 'POST':
        username = request.POST.get("username", False)
        try:
            User.objects.get(username=username)
            data = {'code': '0', 'info': u'用户名已注册'}
            return JsonResponse(data)
        except:
            data = {'code': '1', 'info': u'用户名可用'}
            return JsonResponse(data)


@login_required
def index(request):
    teams = ProjectTeam.objects.all()
    for team in teams:
        key = team.Introduction
        soup = BeautifulSoup(key, "html5lib")
        team.Introduction = soup.text[0:100] + '...'
    introduction = Introduction.objects.get()
    contact = ContactUs.objects.get()
    posters = Poster.objects.all()
    courses = Course.objects.all()
    return render(request, 'home.html',
                  {'teams': teams, 'courses': courses, 'introduction': introduction, 'contact': contact,
                   'posters': posters})


@login_required
def contactUs(request):
    if request.method == 'POST':
        form = myUEditorModelForm(request.POST)
        if form.is_valid():
            blog = form.save()
            ContactUs.objects.all().delete()
            article = ContactUs()
            article.Name = blog.Name
            article.Content = blog.Content
            blog.delete()
            article.save()
            url = '/index/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponse(u"数据校验错误")
    else:
        try:
            article = ContactUs.objects.get()
            form = myUEditorModelForm(instance=article)
        except:
            form = myUEditorModelForm()
        teams = ProjectTeam.objects.all()
        courses = Course.objects.all()
        return render(request, 'editBlog.html', {'form': form, 'teams': teams, 'courses': courses})


@login_required
def introduce(request):
    if request.method == 'POST':
        form = myUEditorModelForm(request.POST)
        if form.is_valid():
            blog = form.save()
            Introduction.objects.all().delete()
            article = Introduction()
            article.Name = blog.Name
            article.Content = blog.Content
            blog.delete()
            article.save()
            url = '/index/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponse(u"数据校验错误")
    else:
        try:
            article = Introduction.objects.get()
            form = myUEditorModelForm(instance=article)
        except:
            form = myUEditorModelForm()
        teams = ProjectTeam.objects.all()
        courses = Course.objects.all()
        return render(request, 'editBlog.html', {'form': form, 'teams': teams, 'courses': courses})


@login_required
def changePoster(request):
    if request.method == 'POST':
        fileForm = FileUploadForm(request.POST, request.FILES)
        if fileForm.is_valid():
            file = Poster()
            file.fileField = fileForm.cleaned_data['file']
            file.save()
        url = request.get_full_path()
        return HttpResponseRedirect(url)
    else:
        teams = ProjectTeam.objects.all()
        introduction = Introduction.objects.get()
        contact = ContactUs.objects.get()
        fileForm = FileUploadForm()
        posters = Poster.objects.all()
        courses = Course.objects.all()
        return render(request, 'poster.html',
                      {'teams': teams, 'introduction': introduction, 'contact': contact, 'fileForm': fileForm,
                       'posters': posters, 'courses': courses})


@login_required
def deletePoster(request, name):
    poster = Poster.objects.get(fileField=name)
    poster.delete()
    url = '/index/changePoster/'
    return HttpResponseRedirect(url)
