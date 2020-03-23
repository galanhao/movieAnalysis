import datetime
import json
import os
import random
import time
from urllib.parse import urlparse

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


from DB.mongdbCli import MongoDBCli
from movieAnalysis.settings import PROXY_SPIDER_LOG_DIR, logger
from proxyManager.models import Proxy
from proxyManager.tasks import task_verifyIP, task_runSpider, clearIP
from proxyManager.utils import getLogInfoList, checkJson, getRandomLogFileName


def index(request):
    # result = task_7yip.delay()
    print("a")

    return HttpResponse("index")




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
class GetIPList(View):
    page_size = 20
    def get(self, request):
        proxys = Proxy.objects.filter(Q(https=1)|Q(http=1))
        m_count = proxys.count()


        content = {
            "m_count":m_count,
            "page_size": self.page_size,
        }
        return render(request, "proxy/ipList.html", content)

    def post(self, request):
        pageIndex = -1
        try:
            pageIndex = int(request.POST.get("pageIndex", -1))-1
        except BaseException as e:
            logger.error(e)
            pass
        if pageIndex == -1:
            return JsonResponse({
                "flag": False,
                "data": "哦豁"
            })
        proxys = Proxy.objects.values(
            "id", "ip", "port", "http", "https", "anonymity",
            "speed", "area", "verify_time", "source"
        ).filter(Q(https=1) | Q(http=1)).order_by("speed")
        start_index = pageIndex*self.page_size
        return JsonResponse({
            "flag":True,
            "data": list(proxys[start_index: start_index+self.page_size])
        })



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
        print("开始调用")
        result = clearIP.delay(getRandomLogFileName("clearIP"))
        print(result)
        return JsonResponse({
            "flag": True,
            "massage": "启动成功"
        })




@csrf_exempt
def runVerifyIP(request):
    print("sss")
    logger.info("得到请求runVerifyIP")
    result = None
    try:
        lf = getRandomLogFileName("verifyIP")
        print("开始调用", lf)
        result = task_verifyIP.delay(lf)
    except BaseException as e:
        print(e)
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






if __name__ == "__main__":
    print(getLogInfoList())



