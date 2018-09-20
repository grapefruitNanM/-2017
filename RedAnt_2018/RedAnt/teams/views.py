# coding:utf-8
from RedAnt.forms import teamForm, myUEditorModelForm, FileUploadForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from RedAnt.models import ProjectTeam, Blog, LearningResources, Photo, Course, log
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
import math


@permission_required('RedAnt.add_projectteam')
@login_required
def teamAdd(request):
    if request.method == 'POST':
        form = teamForm(request.POST)
        if form.is_valid():
            newTeam = form.save()
            newTeam.GroupPhoto = 'photos/LOGO.png'
            newTeam.save()
            url = '/teams/major=' + str(newTeam.id) + '/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponse(u"数据校验错误")
    else:
        editor = teamForm()
        teams = ProjectTeam.objects.all()
        courses = Course.objects.all()
        return render(request, 'teamEdit.html', {'teams': teams, 'editor': editor, 'courses': courses})


def teamMajor(request, name):
    try:
        team = ProjectTeam.objects.get(id=int(name))
    except:
        return HttpResponse(u"项目组不存在")
    if request.method == 'POST':
        fileForm = FileUploadForm(request.POST, request.FILES)
        if fileForm.is_valid():
            file = LearningResources()
            file.Team = ProjectTeam.objects.get(id=name)
            file.teamId = name
            file.fileField = fileForm.cleaned_data['file']
            file.name = file.fileField.name
            file.save()
            newLog = log(User=request.user.username, Content="上传了学习资源 " + file.name + " 。")
            newLog.save()
        url = request.get_full_path()
        return HttpResponseRedirect(url)
    else:
        blogs = Blog.objects.filter(Team=team).order_by('-modify_time')
        teams = ProjectTeam.objects.all()
        fileForm = FileUploadForm()
        resourceList = LearningResources.objects.filter(Team=team).order_by('-date')
        courses = Course.objects.all()
        return render(request, 'projectTeam.html', {'team': team, 'teams': teams,
                                                    'blogs': blogs, 'fileForm': fileForm, 'resourceList': resourceList,
                                                    'courses': courses})


@permission_required('RedAnt.change_projectteam')
@login_required
def edit(request, name):
    if request.method == 'POST':
        form = teamForm(request.POST)
        if form.is_valid():
            team = ProjectTeam.objects.get(id=int(name))
            newTeam = form.save()
            if team.TeamName != newTeam.TeamName:
                users = User.objects.filter(first_name=team.TeamName)
                for user in users:
                    user.first_name = newTeam.TeamName
                    user.save()
            team.TeamName = newTeam.TeamName
            team.OutofTime = newTeam.OutofTime
            team.Introduction = newTeam.Introduction
            newTeam.delete()
            team.save()
            newLog = log(User=request.user.username, Content="编辑 " + team.TeamName + " 信息。")
            newLog.save()
            url = '/teams/major=' + str(team.id) + '/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponse(u"数据校验错误")
    else:
        team = ProjectTeam.objects.get(id=int(name))
        editor = teamForm(instance=team)
        teams = ProjectTeam.objects.all()
        courses = Course.objects.all()
        return render(request, 'teamEdit.html', {'team': team, 'teams': teams, 'editor': editor, 'courses': courses})


@permission_required('RedAnt.delete_projectteam')
@login_required
def delete(request, name):
    team = ProjectTeam.objects.get(id=int(name))
    users = User.objects.filter(first_name=team.TeamName)
    for user in users:
        user.first_name = ''
        user.save()
    team.delete()
    newLog = log(User=request.user.username, Content="删除 " + team.TeamName + " 。")
    newLog.save()
    url = '/index/'
    return HttpResponseRedirect(url)


@permission_required('RedAnt.change_blog')
@login_required
def editBlog(request, name, article):
    if article == 'new':
        if request.method == 'POST':
            form = myUEditorModelForm(request.POST)
            if form.is_valid():
                blog = form.save()
                blog.Team = ProjectTeam.objects.get(id=int(name))
                blog.save()
                newLog = log(User=request.user.username, Content="新建日志 " + blog.Name + " 。")
                newLog.save()
                url = '/teams/major=' + name + '/'
                return HttpResponseRedirect(url)
            else:
                return HttpResponse(u"数据校验错误")
        else:
            form = myUEditorModelForm()
            teams = ProjectTeam.objects.all()
            courses = Course.objects.all()
            return render(request, 'editBlog.html', {'form': form, 'teams': teams, 'courses': courses})
    else:
        if request.method == 'POST':
            form = myUEditorModelForm(request.POST)
            Blog.objects.get(id=article).delete()
            if form.is_valid():
                blog = form.save()
                blog.Team = ProjectTeam.objects.get(id=name)
                blog.save()
                newLog = log(User=request.user.username, Content="编辑日志 " + blog.Name + " 。")
                newLog.save()
                url = '/teams/major=' + name + '/'
                return HttpResponseRedirect(url)
            else:
                return HttpResponse(u"数据校验错误")
        else:
            article = Blog.objects.get(id=article)
            form = myUEditorModelForm(instance=article)
            teams = ProjectTeam.objects.all()
            courses = Course.objects.all()
            return render(request, 'editBlog.html', {'form': form, 'teams': teams, 'courses': courses})


@permission_required('RedAnt.delete_blog')
@login_required
def deleteBlog(request, name, article):
    newLog = log(User=request.user.username, Content="删除日志 " + Blog.objects.get(id=article).Name + " 。")
    newLog.save()
    Blog.objects.get(id=article).delete()
    url = '/teams/major=' + name + '/'
    return HttpResponseRedirect(url)


@permission_required('RedAnt.delete_learningresources')
@login_required
def deleteResource(request, name, file):
    newLog = log(User=request.user.username,
                 Content="删除学习资源 " + LearningResources.objects.get(fileField=file).name + " 。")
    newLog.save()
    LearningResources.objects.get(fileField=file).delete()
    url = '/teams/major=' + name + '/'
    return HttpResponseRedirect(url)


@login_required
def changeImg(request, name):
    if request.method == 'POST':
        fileForm = FileUploadForm(request.POST, request.FILES)
        if fileForm.is_valid():
            team = ProjectTeam.objects.get(id=name)
            photo = Photo()
            photo.fileField = fileForm.cleaned_data['file']
            photo.save()
            newLog = log(User=request.user.username,
                         Content="修改 " + team.TeamName + " 照片。")
            newLog.save()
            try:
                Photo.objects.get(fileField=team.GroupPhoto).delete()
                team.GroupPhoto = photo.fileField
                team.save()
                url = '/index/'
                return HttpResponseRedirect(url)
            except:
                team.GroupPhoto = photo.fileField
                team.save()
                url = '/index/'
                return HttpResponseRedirect(url)
    else:
        editor = FileUploadForm()
        teams = ProjectTeam.objects.all()
        courses = Course.objects.all()
        return render(request, 'teamEdit.html', {'editor': editor, 'teams': teams, 'courses': courses})


def postTolPage(request, name):
    try:
        team = ProjectTeam.objects.get(id=int(name))
    except ProjectTeam.DoesNotExist:
        return HttpResponse(u"项目组不存在")
    tol = len(Blog.objects.filter(Team=team))
    page = math.ceil(tol / 3)
    data = {'tol_page': page}
    return JsonResponse(data)


def postBlogAjax(request, name):
    try:
        team = ProjectTeam.objects.get(id=int(name))
    except ProjectTeam.DoesNotExist:
        return HttpResponse(u"项目组不存在")
    page = int(request.POST["page"])
    blog = Blog.objects.filter(Team=team).order_by('-modify_time')
    resp = []
    for i in range((page - 1) * 3, page * 3):
        if i < len(blog):
            resp.append({'id': blog[i].id, 'name': blog[i].Name, 'year': blog[i].modify_time.year,
                         'month': blog[i].modify_time.month, 'day': blog[i].modify_time.day,
                         'content': blog[i].Content})
    return HttpResponse(json.dumps(resp), content_type="application/json")
