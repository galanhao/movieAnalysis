import sys

import MySQLdb

sys.path.append('C:\\Users\\haowenhao\\Desktop\\biyesheji\\BSv4\\movieAnalysis')
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'movieAnalysis.settings'
django.setup()
from proxyManager.models import Proxy


def get_proxy_https():
    db = MySQLdb.connect("localhost", "root", "password", "ippool", charset='utf8')
    cursor = db.cursor()
    sql = 'select ip, port from proxys where protocol>0 and types<=2 and score>8 and speed<3.5;'
    cursor.execute(sql)
    results = cursor.fetchall()
    # for result in results:
    #     print(result)

    print(results)
    db.close()
    return results
rets = get_proxy_https()


for ret in rets:
    try:
        Proxy.objects.create(ip=ret[0], port=ret[1], source="IPPOOL")
    except:
        pass
