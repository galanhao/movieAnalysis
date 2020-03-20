
from django.conf.urls import url

from proxyManager import views

urlpatterns = [
    url('^index$', views.index, name='index'),
    url('^verifyip$', views.verifyIP, name='verifyIP'),
    url('proxylist', views.proxyList, name="proxyList"),
    url('log/(?P<log_file>\S+)', views.getLog, name="getLog"),
    url('runspider', views.runSpider, name="runSpider"),


]