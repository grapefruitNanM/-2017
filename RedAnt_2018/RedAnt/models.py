# coding:utf-8
#
from django.db import models
from DjangoUeditor.models import UEditorField
from DjangoUeditor.commands import *
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from DUSite import settings
import os
from hashlib import md5


class log(models.Model):
    User = models.CharField(max_length=100)
    Content = models.CharField(max_length=100)
    Time = models.DateTimeField(auto_now=True)


class Introduction(models.Model):
    Name = models.CharField(u'名称', max_length=100)
    Content = UEditorField(u'内容', height=200, width=788, imagePath="introduction/", toolbars="besttome")


class ContactUs(models.Model):
    Name = models.CharField(u'名称', max_length=100)
    Content = UEditorField(u'内容', height=200, width=788, imagePath="contactus/", toolbars="besttome")


class Poster(models.Model):
    fileField = models.FileField(upload_to='index/poster/')


@receiver(post_delete, sender=Poster)
def delete_files(sender, instance, **kwargs):
    files = getattr(instance, 'fileField', '')
    if not files:
        return
    fname = os.path.join(settings.MEDIA_ROOT, str(files))
    if os.path.isfile(fname):
        os.remove(fname)


class Photo(models.Model):
    fileField = models.FileField(upload_to='photos/')


@receiver(post_delete, sender=Photo)
def delete_photos(sender, instance, **kwargs):
    files = getattr(instance, 'fileField', '')
    if not files:
        return
    fname = os.path.join(settings.MEDIA_ROOT, str(files))
    if os.path.isfile(fname):
        os.remove(fname)


class inviteCode(models.Model):
    code = models.CharField(max_length=100)
    ddl = models.CharField(max_length=100)


class ProjectTeam(models.Model):
    TeamName = models.CharField(u'项目组名称', max_length=100, null=True)
    Introduction = UEditorField(u'项目组简介', height=100, width=788, imagePath="team/", toolbars="besttome")
    OutofTime = models.BooleanField(u'历史项目组', default=False)
    GroupPhoto = models.ImageField(upload_to='photos/')


class Blog(models.Model):
    Name = models.CharField(u'名称', max_length=100)
    ImagePath = models.ImageField(null=True)
    Content = UEditorField(u'内容', height=200, width=788, imagePath="blog/",
                           toolbars="full")
    modify_time = models.DateTimeField(auto_now=True)
    Team = models.ForeignKey('ProjectTeam', null=True, on_delete=models.CASCADE, )


def get_upload_path(instance, filename):
    name = instance.Team.TeamName
    return 'Resourses/%s/%s' % (name, filename)


class LearningResources(models.Model):
    Team = models.ForeignKey('ProjectTeam', on_delete=models.CASCADE, )
    teamId = models.CharField(max_length=100, null=True)
    fileField = models.FileField(upload_to=get_upload_path)
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=30, blank=True, null=True)


@receiver(post_delete, sender=LearningResources)
def delete_upload_files(sender, instance, **kwargs):
    files = getattr(instance, 'fileField', '')
    if not files:
        return
    fname = os.path.join(settings.MEDIA_ROOT, str(files))
    if os.path.isfile(fname):
        os.remove(fname)


class Post(models.Model):
    postedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    postNum = models.CharField(max_length=100)
    name = models.CharField(u'名称', max_length=100)
    modify_time = models.DateTimeField(auto_now=True)


class lPost(models.Model):
    postedBy = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    Content = UEditorField(u'回复', height=200, width=788, imagePath="forum/",
                           toolbars="besttome")
    modify_time = models.DateTimeField(auto_now=True)
    post = models.ForeignKey('post', null=True, on_delete=models.CASCADE, )


class Course(models.Model):
    Name = models.CharField(u'课程名称', max_length=100, null=True)
    Introduction = UEditorField(u'课程简介', height=100, width=788, imagePath="course/", toolbars="besttome")


class ZhangJieSmallPic(models.Model):
    file = models.FileField(upload_to=get_upload_path)
    zhangJiesmall = models.ForeignKey('ZhangJieSmall', on_delete=models.CASCADE)

    @staticmethod
    def save_file(f):
        m = md5()
        for i in f.chunks():
            m.update(i)
        name = m.hexdigest() + '.' + f.name.split('.')[-1]
        fp = os.path.join(
            os.path.dirname(__file__),
            '../Media/course/%s' % name
        )
        if not os.path.exists(fp):
            with open(fp, 'wb+') as fw:
                for i in f.chunks():
                    fw.write(i)
        return name

    def path(self):
        return '/Media/course/%s' % str(self.file)

    def __str__(self):
        return self.file.path


@receiver(post_delete, sender=ZhangJieSmallPic)
def deletePPT(sender, instance, **kwargs):
    files = getattr(instance, 'file', '')
    if not files:
        return
    fname = os.path.join(
        os.path.dirname(__file__),
        '..../Media/course/%s' % str(files)
    )
    if os.path.isfile(fname):
        os.remove(fname)


class ZhangJieSmall(models.Model):
    name = models.CharField(max_length=21)
    video = models.FileField(upload_to=get_upload_path)
    video_desc = models.CharField(max_length=1024, default='', blank=True)
    content = models.CharField(max_length=2048, default='', blank=True)
    zhangJie = models.ForeignKey('ZhangJie', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ZhangJie(models.Model):
    kecheng = models.CharField(max_length=21)
    name = models.CharField(max_length=21)
    details = models.ManyToManyField(ZhangJieSmall)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
