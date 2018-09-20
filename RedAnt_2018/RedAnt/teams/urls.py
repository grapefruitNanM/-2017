from django.conf.urls import include, url
import RedAnt.teams.views as views

urlpatterns = [
    url(r'major=(?P<name>.*)/delete/resource=(?P<file>.*)/', views.deleteResource),
    url(r'major=(?P<name>.*)/delete/article=(?P<article>.*)/', views.deleteBlog),
    url(r'major=(?P<name>.*)/article=(?P<article>.*)/', views.editBlog),
    url(r'major=(?P<name>.*)/edit/', views.edit),
    url(r'major=(?P<name>.*)/delete/', views.delete),
    url(r'major=(?P<name>.*)/changeImg/', views.changeImg),
    url(r'major=(?P<name>.*)/post_tol_page', views.postTolPage),
    url(r'major=(?P<name>.*)/post_blog_ajax', views.postBlogAjax),
    url(r'major=(?P<name>.*)/', views.teamMajor),
    url(r'operating=new/', views.teamAdd),
]
