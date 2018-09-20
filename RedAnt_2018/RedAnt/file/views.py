#coding:utf-8
import urllib.request

def getFile(request):
    if request.method == 'get':
        file = urllib.unquote(request.GET.get('term')).decode('utf8')
        return HttpResponseRedirect('media/course/%s' % file)