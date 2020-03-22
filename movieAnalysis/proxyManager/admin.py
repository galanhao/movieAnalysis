from django.contrib import admin

# Register your models here.
from proxyManager.models import Proxy


class ProxyAdmin(admin.ModelAdmin):
    list_display = ["id", "ip", "port", "html_http", "html_https", "html_anonymity", "html_speed", "area", "verify_time", ]
    list_filter = ('http', "https", "anonymity")


admin.site.register(Proxy, ProxyAdmin)