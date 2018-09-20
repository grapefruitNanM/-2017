from django.conf.urls import include, url
import RedAnt.personalAccount.views as views

urlpatterns = [
    url(r'checkPrepsw/',views.checkPrepsw),
    url(r'changeImg/',views.accountImgChange),
    url(r'',views.account_manager),
]