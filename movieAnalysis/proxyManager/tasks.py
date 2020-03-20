import sys
import os
from scrapy import cmdline
import time
from movieAnalysis.settings import BASE_DIR
SCRAPY_DIR = os.path.join(BASE_DIR, "spiders\\proxySpider\\proxySpider")


from celery import shared_task

@shared_task
def task_7yip():
    os.chdir(SCRAPY_DIR)
    cmdline.execute('scrapy crawl genericSpider -a cn=kuaidaili -a ei=15'.split())

@shared_task
def addd(s):
    print("s", s)
    time.sleep(2)
    return "OK"

@shared_task
def task_verifyIP(log_file):
    os.chdir(SCRAPY_DIR)
    cmdline.execute('scrapy crawl verify -s LOG_FILE={}'.format(log_file).split())

@shared_task
def task_runSpider(spider_name, log_file, param):
    os.chdir(SCRAPY_DIR)
    cmdline.execute('scrapy crawl genericSpider -a cn={}  -s LOG_FILE={} {}'.format(spider_name, log_file, param).split())

