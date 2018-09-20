# coding:utf-8
import datetime
import json
import os
import pythoncom
import random
import re
import urllib.request
import win32com
import win32com.client
from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from pprint import pprint

import DUSite
from RedAnt import models as m
from RedAnt.forms import teamForm, myUEditorModelForm, FileUploadForm, CourseForm, smallCourseForm
from RedAnt.models import ProjectTeam, Blog, LearningResources, Course

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/Media/course/'


@permission_required('RedAnt.add_ProjectTeam')
@login_required
def courseAdd(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            newCourse = form.save()
            newCourse.save()
            url = '/courses/major=' + str(newCourse.id)
            return HttpResponseRedirect(url)
        else:
            return HttpResponse(u"数据校验错误")
    else:
        editor = CourseForm()
        teams = ProjectTeam.objects.all()
        courses = Course.objects.all()
        return render(request, 'courseEdit.html', {'teams': teams, 'editor': editor,'courses': courses})


@login_required
def courseEdit(request, name):
    if request.method == 'POST':
        Introduction = request.POST.get('Introduction')
        course = Course.objects.get(id=name)
        course.Introduction = Introduction
        course.save()
        url = '/courses/major=' + str(course.id) +'/'
        return HttpResponseRedirect(url)
    else:
        course = Course.objects.get(id=name)
        editor = smallCourseForm(instance=course)
        courses = Course.objects.all()
        teams = ProjectTeam.objects.all()
        return render(request, 'courseEdit.html', {'courses': courses, 'teams': teams, 'editor': editor})


def courseMajor(request, name):
    teams = ProjectTeam.objects.all()
    courses = Course.objects.all()
    course = Course.objects.get(id=name)
    zjs = m.ZhangJie.objects.filter(course=course)
    context = {
        'teams': teams,
        'zjs': zjs,
        'kecheng': name,
        'course': course,
        'courses': courses,
        'pics': None
    }
    if request.GET.get('operating', None) == 'delete':
        course.delete()
        try:
            course = Course.objects.all()
            context['course'] = course[0]
            return HttpResponseRedirect('/courses/major=%s' % course[0].id)
        except:
            return HttpResponseRedirect('/index/')
    if request.GET.get('zjs_id', None):
        zjsmall = m.ZhangJieSmall.objects.get(id=request.GET['zjs_id'])
        pics = m.ZhangJieSmallPic.objects.filter(zhangJiesmall=zjsmall)
        if request.GET.get('operating', None) == 'delzjs':
            zjsmall.delete()
            return HttpResponseRedirect('/courses/major=%s' % name)
        context['zjsmall'] = zjsmall
        context['zj'] = m.ZhangJieSmall.objects.get(id=request.GET['zjs_id']).zhangjie_set.all()[0]
        context['pics'] = pics
        return render(request, 'course_detail.html', context=context)
    elif zjs.exists() and zjs[0].details.exists():
        context['zjsmall'] = zjs[0].details.all()[0]
        context['zj'] = zjs[0]
    return render(request, 'course.html', context=context)


@login_required
def zhangjie_add(req):
    teams = ProjectTeam.objects.all()
    courses = Course.objects.all()
    if req.method == 'GET':
        courseName = req.GET['kecheng']
        zjs = m.ZhangJie.objects.filter(course=courseName)
        course = Course.objects.get(id=courseName)
        return render(req, 'course_zhangjie_add.html', {
            'teams': teams,
            'zjs': zjs,
            'kecheng': req.GET['kecheng'],
            'course': course,
            'courses': courses
        })
    zj, created = m.ZhangJie.objects.get_or_create(
        kecheng=req.POST['kecheng'],
        name=req.POST['name'],
        course=Course.objects.get(id=req.GET['kecheng']))
    return HttpResponseRedirect('/courses/major=%s' % req.POST['kecheng'])


@login_required
def zhangjie_del(req):
    m.ZhangJie.objects.filter(id=req.GET['zj_id']).delete()
    return HttpResponseRedirect('/courses/major=%s/' % (req.GET['kecheng']))


@login_required
def zhangjie_small_add(req):
    teams = ProjectTeam.objects.all()
    courses = Course.objects.all()
    if req.method == 'GET':
        kecheng = req.GET['kecheng']
        course = Course.objects.get(id=kecheng)
        zjs = m.ZhangJie.objects.filter(course=kecheng)
        return render(req, 'course_zhangjie_small_add.html', {
            'teams': teams,
            'zjs': zjs,
            'zj': req.GET['zj'],
            'kecheng': kecheng,
            'course': course,
            'zjs_id': req.GET.get('zjs_id', ''),
            'zjsmall': m.ZhangJieSmall.objects.get(
                id=req.GET['zjs_id']) if req.GET.get('zjs_id', '') else '',
            'type_': req.GET.get('type', ''),
            'courses': courses
        })

    zj = m.ZhangJie.objects.get(course=req.POST['kecheng'], name=req.POST['zj'])

    zjsp_s = []
    ppt = req.FILES.get('pics')
    if req.POST.get('zjs_id', None):
        zjs = m.ZhangJieSmall.objects.get(id=req.POST['zjs_id'])
        oldzjsp = m.ZhangJieSmallPic.objects.filter(zhangJiesmall=zjs)
    else:
        zjs = m.ZhangJieSmall()
        zjs.name = req.POST['name']
        zjs.zhangJie = zj
        oldzjsp = None


    try:
        if ppt:
            fname = m.ZhangJieSmallPic.save_file(ppt)
            pythoncom.CoInitialize()
            powerpoint = win32com.client.Dispatch('PowerPoint.Application')
            powerpoint.Visible = 1
            pptFileName = path + fname
            ppt = powerpoint.Presentations.Open(pptFileName)
            ppt.SaveAs(pptFileName + '_result.jpg', 17)
            powerpoint.Quit()
            pythoncom.CoUninitialize()
            fns = os.listdir(path + fname + '_result')
            zjs.save()
            if oldzjsp:
                for p in oldzjsp:
                    p.delete()
            for f in sorted(fns,key= lambda x:int(x[3:-4])):
                zjsp = m.ZhangJieSmallPic()
                zjsp.file = fname+'_result/'+ f
                zjsp.zhangJiesmall = zjs
                zjsp.save()
                zjsp_s.append(zjsp)
    except:
        return HttpResponse(u"PPT上传错误,请重新上传或更换PPT")
		
    if req.FILES.get('video', None):
        zjs.video = m.ZhangJieSmallPic.save_file(req.FILES['video'])
    if req.POST.get('video_desc', None):
        zjs.video_desc = req.POST['video_desc']
    if req.POST.get('content', None):
        zjs.content = req.POST['content']
    zjs.save()
    zj.details.add(zjs)
    return HttpResponseRedirect('/courses/major=%s?zjs_id=%s' % (req.POST['kecheng'], zjs.id))
