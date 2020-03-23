import sys

from DB.mongdbCli import MongoDBCli

sys.path.append('C:\\Users\\haowenhao\\Desktop\\biyesheji\\BSv4\\movieAnalysis')
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'movieAnalysis.settings'
django.setup()

import subprocess
import sys
import os
from scrapy import cmdline
import time
from movieAnalysis.settings import PROXY_SPIDER_DIR, PROXY_SPIDER_LOG_DIR

from celery import shared_task, task

from proxyManager.models import Proxy
from proxyManager.utils import getRandomLogFileName

@shared_task
def testWriteFile():
    test_file = os.path.join(PROXY_SPIDER_LOG_DIR, "test")
    with open(test_file, 'w')as fp:
        fp.write("%s"%time.time())
    return "6666"




@shared_task
def clearIP(log_file=None):
    if log_file==None:
        log_file = getRandomLogFileName("clearIP-beat")

    proxys = Proxy.objects.filter(
        https=0, http=0
    )
    log_file_abs = os.path.join(PROXY_SPIDER_LOG_DIR, log_file)
    with open(log_file_abs, 'w', encoding="utf-8")as fp:
        fp.write("\t %-15s   %-6s  %-10s %-10s %-34s %-10s %-10s %-10s\n"
              % ("ip", "port", "protocol", "anonymity",
                 "verify_time", "http", "https", "source"))
        fp.write("\t"+("-" * 112)+"\n")
        for proxy in proxys:
            fp.write("\t %-15s   %-6s  %-10s %-10s %-34s %-10s %-10s %-10s\n"
                  % (proxy.ip, proxy.port, proxy.protocol, proxy.anonymity,
                     proxy.verify_time, proxy.http, proxy.https, proxy.source))
    try:
        proxys.delete()
    except:
        return "删除失败"
    return "删除成功"

@shared_task
def task_verifyIP(log_file=None):
    print("task_verifyIP 接收到的值", log_file)
    if log_file==None:
        log_file = getRandomLogFileName("verifyIP-beat")
    os.chdir(PROXY_SPIDER_DIR)
    log_file_abs = os.path.join(PROXY_SPIDER_LOG_DIR, log_file)
    cmd = 'scrapy crawl verify -s LOG_FILE={}'.format(log_file_abs)
    print(cmd)
    # os.system(cmd)
    subprocess.Popen(cmd)
    # cmdline.execute(cmd.split())
    return log_file

@shared_task
def task_runSpider(spider_name, log_file=None, param=""):
    if log_file==None:
        log_file = getRandomLogFileName(spider_name+"-beat")
        db = MongoDBCli()
        spider_config = db.getOneSpiderFromSpiderName(spider_name)
        param = "-a si={} -a ei={}".format(
            spider_config["startIndex"],
            spider_config["endIndex"],
        )
    os.chdir(PROXY_SPIDER_DIR)
    log_file_abs = os.path.join(PROXY_SPIDER_LOG_DIR, log_file)
    print(log_file_abs)
    cmd = 'scrapy crawl genericSpider -a cn={}  -s LOG_FILE={} {}'.format(spider_name, log_file_abs, param)
    print(cmd)
    # cmdline.execute(cmd.split())
    # subprocess.Popen("notepad")
    # os.system(cmd)
    subprocess.Popen(cmd)
    return log_file
