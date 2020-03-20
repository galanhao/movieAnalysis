def getArea_ip138(response):
    ret = None
    # print(response.body)
    tmp  = response.xpath('/html[1]/body[1]/p[1]/text()')
    # print(tmp)
    ret = tmp.extract_first("").strip()
    return ret

def getArea_chinaz(response):
    ret = None
    # print(response.body)
    # print(response.xpath('/html[1]/body[1]/div[2]/div[1]/div[3]/div[2]/p/text()'))
    tmp  = response.xpath('/html[1]/body[1]/div[2]/div[1]/div[3]/div[2]/p[2]/span[4]/text()')
    # print(tmp)
    ret = tmp.extract_first("").strip()
    return ret


def getArea_default(response):
    print("默认 getArea")
    return  None