import sys
import time

sys.path.append('C:\\Users\\haowenhao\\Desktop\\biyesheji\\BSv4\\movieAnalysis')
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'movieAnalysis.settings'
django.setup()

from django.db.models import Q

from proxyManager.models import Proxy

if __name__ == "__main__":
    st = time.time()
    proxys = Proxy.objects.values().all()[:1000]
    print(Proxy.objects.name)
    # for c in proxys:
    #     print(c.html_http())
    print(proxys)
    print(time.time()-st)