import datetime
import random
import time
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from DB.mongdbCli import MongoDBCli
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
        "spiderTasks": []
    }
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

    return render(request, "proxy/proxyList.html", context=content)


def getRandomLogFileName(name=""):
    time_str = time.strftime("%Y%m%d_%H%M%S")
    random_str = "".join([str(random.randint(0, 9)) for x in range(6)])
    ret = time_str+"_"+name+"_"+random_str+".log"
    with open(ret, 'w', encoding="utf-8")as fp:
        pass
    return ret


def runSpider(request):
    spider_name = request.POST.get("spiderName", None)
    if spider_name == None:
        return HttpResponse("错误的请求")
    db = MongoDBCli()
    spider_config = db.getOneSpiderConfigFromSpiderName(spider_name)
    if spider_name == None:
        return HttpResponse("没有这个爬虫")
    result = task_runSpider.delay()
    return HttpResponse(result)

if __name__ == "__main__":
    print(getRandomLogFileName("kuaidaiassssssaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaasssssssssli"))



