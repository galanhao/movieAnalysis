import datetime
import json
import os
import random
import time
from urllib.parse import urlparse

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


from DB.mongdbCli import MongoDBCli
from movieAnalysis.settings import PROXY_SPIDER_LOG_DIR
from proxyManager.models import Proxy
from proxyManager.tasks import task_verifyIP, task_runSpider, clearIP


def index(request):
    # result = task_7yip.delay()
    print("a")

    return HttpResponse("index")


def verifyIP(request):
    lf = "s.log"
    result = task_verifyIP.delay(lf)
    return HttpResponse(result)


def proxyList(request):
    db = MongoDBCli()
    spider_list = db.getAllSpider()
    content = {
        "spiderTasks": [],
        "taskList": [],
    }
    def __sortBydatetime(elem):
        return elem["time"]
    for spider in spider_list:
        # print(spider)
        tmp = {}
        tmp["name"] = spider["name"]
        tmp["url"] = urlparse(spider["config"]["url"]).scheme+"://"+urlparse(spider["config"]["url"]).netloc
        tmp["description"] = spider["description"]
        tmp["recentTime"] = datetime.datetime.now()
        tmp["spiderName"] = spider["config"]["name"]
        tmp["useRange"] = spider["config"]["useRange"]
        tmp["startIndex"] = spider["startIndex"]
        tmp["endIndex"] = spider["endIndex"]
        content["spiderTasks"].append(tmp)
    content["taskList"] = getLogInfoList()
    content["taskList"].sort(key=__sortBydatetime, reverse=True)
    return render(request, "proxy/proxyList.html", context=content)

def getLog(request, log_file):
    print(log_file)
    if log_file in [x["fileName"] for x in getLogInfoList()]:
        data = "not Found"
        with open(os.path.join(PROXY_SPIDER_LOG_DIR, log_file), 'r', encoding="utf-8")as fp:
            data = fp.read()
        # print(data)
        return HttpResponse(data, content_type="text/plain,charset=utf-8", charset="utf-8")
    return HttpResponse("not Found")

@method_decorator(csrf_exempt, name='dispatch')
class EditSpiderConfig(View):
    def get(self, request, spider_name):
        # print(time.time())
        # print(request.path)
        db = MongoDBCli()
        spider = db.getOneSpiderFromSpiderName(spider_name)
        # print("spider", spider)
        if spider == None:
            return render(request, '404.html')
        content = {
            "spider": spider,
            "spider_config_json": json.dumps(spider["config"]),

        }
        # print("content", content)
        return render(request, 'proxy/editSpiderConfig.html', context=content)

    def post(self, request, spider_name):
        # receive_spider = json.loads()
        db = MongoDBCli()
        spider = db.getOneSpiderFromSpiderName(spider_name)
        if spider == None:
            return JsonResponse({
                "flag": False,
                "massage": "没有这个爬虫",
            })
        r_tmp = checkJson(request)
        # print(r_tmp)
        if  r_tmp== False:
            return JsonResponse({
                "flag": False,
                "massage": "spider info 参数错误",
            })
        # print(spider, "\n>>\n", r_tmp)
        db_ret = db.setOneSpider(r_tmp)
        if db_ret != None:
            return JsonResponse({"flag": True, "massage": "OK"})
        return JsonResponse({"flag": False, "massage": "编辑错误"})


@method_decorator(csrf_exempt, name='dispatch')
class NowSpiderConfig(View):

    def get(self, request):
        return render(request, "proxy/addSpiderConfig.html")


    def post(self,request):
        receive_data = checkJson(request)
        if receive_data == False:
            return JsonResponse({
                "flag": False,
                "massage": "spider info 参数错误",
            })
        db = MongoDBCli()
        db_ret = db.setOneSpider(receive_data)
        if db_ret != None:
            return JsonResponse({"flag": True, "massage": "OK"})
        return JsonResponse({"flag": False, "massage": "编辑错误"})






def getRandomLogFileName(name=""):
    time_str = time.strftime("%Y%m%d_%H%M%S")
    random_str = "".join([str(random.randint(0, 9)) for x in range(6)])
    ret = time_str+"_"+name+"_"+random_str+".log"
    return ret


@method_decorator(csrf_exempt, name='dispatch')
class ClearIP(View):
    def get(self, request):
        proxys = Proxy.objects.values("ip", "port").filter(
            https=0, http=0
        )
        ret = {
            "data": list(proxys)
        }
        return JsonResponse(ret)

    def post(self, request):
        result = clearIP.delay(getRandomLogFileName("clearIP"))
        print(result)
        return JsonResponse({
            "flag": True,
            "massage": "启动成功"
        })




@csrf_exempt
def runVerifyIP(request):
    result = None
    try:
        result = task_verifyIP.delay(getRandomLogFileName("verifyIP"))
    except BaseException as e:
        logger.error(e)
    if result == None:
        return JsonResponse({
            "flag": False,
            "massage": "启动失败"
        })
    return JsonResponse({
            "flag": True,
            "massage": "启动成功"
        })

@csrf_exempt
def runSpider(request):
    print(request.POST)
    spider_name = request.POST.get("spiderName", None)

    if spider_name == None:
        return HttpResponse("错误的请求")
    db = MongoDBCli()
    spider_config = db.getOneSpiderFromSpiderName(spider_name)
    if spider_config == None:
        return HttpResponse("没有这个爬虫")
    result = "a"
    result = task_runSpider.delay(
        spider_config["config"]["name"],
        getRandomLogFileName(spider_config["config"]["name"]),
        "-a si={} -a ei={}".format(
            spider_config["startIndex"],
            spider_config["endIndex"],
        )
    )
    return HttpResponse(result)
    # return JsonResponse(spider_config)

def getLogInfoList():
    dlst = os.listdir(PROXY_SPIDER_LOG_DIR)
    ret_list = []
    for c in dlst:
        if c.endswith(".log"):
            title_tmp = c[:-4]
            list_tmp  = title_tmp.split("_")
            if len(list_tmp)==4:
                try:
                    ret_list.append({
                        "time": datetime.datetime.fromtimestamp(time.mktime(time.strptime(list_tmp[0]+"_"+list_tmp[1],"%Y%m%d_%H%M%S"))),
                        "name": list_tmp[2],
                        "fileName": c}
                    )
                except BaseException as e:
                    print(e)
    return ret_list


def checkJson(request):
    receive_spider = json.loads(request.body)
    # print(receive_spider)
    if receive_spider.get("name", False) == False:
        return False
    if receive_spider.get("description", False) == False:
        return False
    if receive_spider.get("startIndex", False) == False:
        return False
    if receive_spider.get("endIndex", False) == False:
        return False
    if receive_spider["config"].get("name", False) == False:
        return False
    if receive_spider["config"].get("url", False) == False:
        return False
    if receive_spider["config"].get("header", False) == False:
        return False
    if receive_spider["config"].get("oneLine", False) == False:
        return False
    if receive_spider["config"].get("ip", False) == False:
        return False
    if receive_spider["config"].get("port", False) == False:
        return False
    if receive_spider["config"].get("useRange", False) == False:
        return False
    return receive_spider

if __name__ == "__main__":
    print(getLogInfoList())
    import logging

    logger = logging.getLogger('log')

    logger.info('请求成功！ res')

    logger.error('请求出错：{}')


