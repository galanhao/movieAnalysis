import datetime
import json
import os
import random
import time

from movieAnalysis.settings import PROXY_SPIDER_LOG_DIR


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


def getRandomLogFileName(name=""):
    time_str = time.strftime("%Y%m%d_%H%M%S")
    random_str = "".join([str(random.randint(0, 9)) for x in range(6)])
    ret = time_str+"_"+name+"_"+random_str+".log"
    return ret