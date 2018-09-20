# coding:utf-8
from django import forms
from DjangoUeditor.widgets import UEditorWidget
from DjangoUeditor.forms import UEditorField, UEditorModelForm
from .models import Blog, ProjectTeam, lPost, Course


class teamForm(UEditorModelForm):
    class Meta:
        model = ProjectTeam
        fields = ('TeamName', 'Introduction', 'OutofTime')
        widgets = {
            "TeamName": forms.TextInput(attrs={"style": "width:788px;"}),
            # 直接设置style或者某项属性改变样式，记得字典格式，赋值给attrs
        }


class myUEditorModelForm(UEditorModelForm):
    class Meta:
        model = Blog
        fields = ('Name', 'Content')
        widgets = {
            "Name": forms.TextInput(attrs={"style": "width:788px;"}),
            # 直接设置style或者某项属性改变样式，记得字典格式，赋值给attrs
        }


class postForm(UEditorModelForm):
    class Meta:
        model = lPost
        fields = ('Content',)


class FileUploadForm(forms.Form):
    file = forms.FileField(label='图片')

    class Meta:
        widgets = {
            "file": forms.TextInput(attrs={"class": "files"}),
            # 直接设置style或者某项属性改变样式，记得字典格式，赋值给attrs
        }


class CourseForm(UEditorModelForm):
    class Meta:
        model = Course
        fields = ('Name', 'Introduction')


class smallCourseForm(UEditorModelForm):
    class Meta:
        model = Course
        fields = ('Introduction',)
