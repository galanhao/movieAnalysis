import json

from proxySpider.confs.paramConf import SPEED_ERROR


def getAnonymity_httpbin(response):
    try:
        if response:
            download_latency = response.meta.get("download_latency", SPEED_ERROR)
            speed = '%.3f' % download_latency
            r_dict = json.loads(response.body)
            print(r_dict)
            headers = r_dict.get('headers', '')
            ip = r_dict.get('origin')
            proxy_connection = headers.get('Proxy-Connection', None)
            if ',' in ip:
                types = 3  # 透明
            elif proxy_connection:
                types = 2  # 普匿
            else:
                types = 1  # 高匿
            return True, types, speed
    except BaseException as ex:
        print(ex)
        pass
    return False, 0, 0

def getProtocol_default(response):
    print("这是默认getProtocol")
    return False, 0, 0