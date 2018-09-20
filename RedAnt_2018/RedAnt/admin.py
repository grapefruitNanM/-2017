#coding: utf-8
from django.contrib import admin
from RedAnt.models import *

class BlogAdmin(admin.ModelAdmin):
    list_display = ("Name","Content","ImagePath")


#注册管理
admin.site.register(Blog,BlogAdmin)
