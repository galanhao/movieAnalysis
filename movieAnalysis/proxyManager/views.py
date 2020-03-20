import datetime
import os
import random
import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from scrapy.http import TextResponse

from DB.mongdbCli import MongoDBCli
from movieAnalysis.settings import PROXY_SPIDER_LOG_DIR
from proxyManager.tasks import task_7yip, addd, task_verifyIP, task_runSpider


def index(request):
    # result = task_7yip.delay()
    print("a")
    # result = addd.delay("s")
    result = task_7yip.delay()
    print(result)
    return HttpResponse(result)


def verifyIP(request):
    lf = "s.log"
    result = task_verifyIP.delay(lf)
    return HttpResponse(result)


def proxyList(request):
    db = MongoDBCli()
    spider_list = db.getProxySpider()
    content = {
        "spiderTasks": [],
        "taskList": [],
    }
    def __sortBydatetime(elem):
        return elem["time"]
    for spider in spider_list:
        print(spider)
        tmp = {}
        tmp["name"] = spider["name"]
        tmp["url"] = spider["config"]["url"]
        tmp["description"] = spider["description"]
        tmp["recentTime"] = datetime.datetime.now()
        tmp["spiderName"] = spider["config"]["name"]
        tmp["status"] = True
        content["spiderTasks"].append(tmp)
    content["taskList"] = getLogInfoList()
    content["taskList"].sort(key=__sortBydatetime, reverse=False)
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




def getRandomLogFileName(name=""):
    time_str = time.strftime("%Y%m%d_%H%M%S")
    random_str = "".join([str(random.randint(0, 9)) for x in range(6)])
    ret = time_str+"_"+name+"_"+random_str+".log"
    # with open(ret, 'w', encoding="utf-8")as fp:
    #     pass
    return ret

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
        "-a si={} -a ei=2".format(
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

if __name__ == "__main__":
    print(getLogInfoList())


