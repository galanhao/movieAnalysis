from proxySpider.confs.paramConf import SPEED_ERROR


def responseTest_default(response):
    if response and response.status == 200:
        speed = '%.3f' % response.meta.get("download_latency", SPEED_ERROR)
        return True, speed
    return False, SPEED_ERROR
