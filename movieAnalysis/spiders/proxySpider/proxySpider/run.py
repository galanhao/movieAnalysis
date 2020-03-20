import sys
sys.path.append('C:\\Users\\haowenhao\\Desktop\\biyesheji\\BSv4\\movieAnalysis')
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'movieAnalysis.settings'
django.setup()



from django.db.models import Q

from proxyManager.models import Proxy



from scrapy import cmdline
# cmdline.execute('scrapy crawl genericSpider -a cn=kuaidaili -a ei=15'.split())


print("开始了")


def verifyIP():
    cmdline.execute('scrapy crawl verify'.split())

def genericSpider(spider_name, start_index=1, end_index=5):
    cmdline.execute('scrapy crawl genericSpider -a cn={} -a si={} -a ei={}'.format(spider_name, start_index, end_index).split())
def clearProxy():
    print("即将删除以下Proxy：")
    proxys = Proxy.objects.filter(
        https=0, http=0
    )
    print("\t %-15s   %-6s  %-10s %-10s %-12s %-10s %-10s %-10s"
          % ("ip", "port", "protocol", "anonymity",
             "verify_time", "http", "https", "source"))
    print("\t", "-" * 105)
    for proxy in proxys:
        print("\t %-15s   %-6s  %-10s %-10s %-12s %-10s %-10s %-10s"
              % (proxy.ip, proxy.port, proxy.protocol, proxy.anonymity,
                 proxy.verify_time, proxy.http, proxy.https, proxy.source))
    proxys.delete()
    print("删除完成")
# genericSpider("7yip", 1, 1)
# clearProxy()
verifyIP()








