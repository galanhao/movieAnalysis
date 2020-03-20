import sys
import os
from scrapy import cmdline
import time
from movieAnalysis.settings import PROXY_SPIDER_DIR, PROXY_SPIDER_LOG_DIR

from celery import shared_task

@shared_task
def task_7yip():
    os.chdir(PROXY_SPIDER_DIR)
    cmdline.execute('scrapy crawl genericSpider -a cn=kuaidaili -a ei=15'.split())

@shared_task
def addd(s):
    print("s", s)
    time.sleep(2)
    return "OK"

@shared_task
def task_verifyIP(log_file):
    os.chdir(PROXY_SPIDER_DIR)
    log_file_abs = os.path.join(PROXY_SPIDER_LOG_DIR, log_file),
    cmdline.execute('scrapy crawl verify -s LOG_FILE={}'.format(log_file_abs).split())
    return log_file

@shared_task
def task_runSpider(spider_name, log_file, param):
    os.chdir(PROXY_SPIDER_DIR)
    log_file_abs = os.path.join(PROXY_SPIDER_LOG_DIR, log_file)
    print(log_file_abs)
    cmd = 'scrapy crawl genericSpider -a cn={}  -s LOG_FILE={} {}'.format(spider_name, log_file_abs, param)
    print(cmd)
    # cmdline.execute(cmd.split())
    os.system(cmd)
    return log_file
