import sys
sys.path.append('C:\\Users\\haowenhao\\Desktop\\biyesheji\\BSv4\\movieAnalysis')
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'movieAnalysis.settings'
django.setup()
import datetime
import time


from proxyManager.models import Proxy
from django.db.models import Q





EXPERT_TIME = 60*60*3
EXPERT_TIME = 60*60*1.5
proxys = Proxy.objects.values("ip", "port", "http", "https", "verify_time").filter(
    Q(Q(http=-1)|Q(https=-1))|Q(verify_time__lte=datetime.datetime.fromtimestamp(time.time()-EXPERT_TIME))
)[:20]
print(datetime.datetime.fromtimestamp(time.time()-EXPERT_TIME))

for c in proxys:
    print(c, c["verify_time"])




