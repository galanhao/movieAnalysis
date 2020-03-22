
from django.conf.urls import url

from proxyManager import views

urlpatterns = [
    url('^index$', views.index, name='index'),

    url('proxylist', views.proxyList, name="proxyList"),
    url('log/(?P<log_file>\S+)', views.getLog, name="getLog"),



    url('config/edit/(?P<spider_name>\S+)', views.EditSpiderConfig.as_view(), name="editSpiderConfig"),
    url('config/new/', views.NowSpiderConfig.as_view(), name="newSpiderConfig"),



    url('clearip', views.ClearIP.as_view(), name="clearIP"),
    url('runspider', views.runSpider, name="runSpider"),
    url('^verifyip$', views.runVerifyIP, name='runVerifyIP'),


]