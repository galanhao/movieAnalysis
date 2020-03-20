from proxySpider.utils.getAnonymitys import getAnonymity_httpbin
from proxySpider.utils.getAreas import getArea_chinaz
from proxySpider.utils.responseTests import responseTest_default

HTTP_TEST_LIST = [
    {
        "url": "http://tool.chinaz.com/",
        "header": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # "Cookie": "__guid=149221043.262733545342315140.1583550179816.1826; UM_distinctid=170b2f22b75548-0cc1c8d45db6d3-3c604504-1fa400-170b2f22b7656f; qHistory=aHR0cDovL2lwLnRvb2wuY2hpbmF6LmNvbS9pcGJhdGNoL19JUOaJuemHj+afpeivonxodHRwOi8vaXAudG9vbC5jaGluYXouY29tX0lQL0lQdjbmn6Xor6LvvIzmnI3liqHlmajlnLDlnYDmn6Xor6J8aHR0cDovL3Rvb2wuY2hpbmF6LmNvbV/nq5nplb/lt6Xlhbd8aHR0cDovL3BpbmcuY2hpbmF6LmNvbV9QaW5n5qOA5rWLfGh0dHA6Ly90b29sLmNoaW5hei5jb20vZG5zL19EbnPmn6Xor6I=; Hm_lvt_aecc9715b0f5d5f7f34fba48a3c511d6=1584539529; CNZZDATA5082706=cnzz_eid%3D16155119-1556339140-%26ntime%3D1584590871; mainurl=%20; monitor_count=3",
            "Host": "tool.chinaz.com",
            "Pragma": "no-cache",
            "Referer": "http://tool.chinaz.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        },
        "callbalk": responseTest_default,
    },
    {
        "url": "http://h.4399.com/",
        "header": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # "Cookie": "UM_distinctid=16f84db331a281-01095c49abe8b8-3c604504-1fa400-16f84db331b407; Hm_lvt_334aca66d28b3b338a76075366b2b9e8=1578481956; _4399stats_vid=15784819791801270; __guid=10391148.1819736692102135300.1584592610757.76; monitor_count=1; _gprp_c=""; Hm_lvt_4709397063c7287bcdfca0bdd6200e16=1584592612; Hm_lpvt_4709397063c7287bcdfca0bdd6200e16=1584592612",
            "Host": "h.4399.com",
            "Pragma": "no-cache",
            "Referer": "https://www.baidu.com/link?url=bjvBj9ahWqAWfyxk5MZ-G9e88lVjB8VVwPuztE8RgDy&wd=&eqid=f4b0367200058e90000000055e72f6d9",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        },
        "callbalk": responseTest_default,
    },
    {
        "url": "http://site.baidu.com/",
        "header": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # "Cookie": "BAIDUID=1F0227587C7DE38C985A29282BA65D3C:FG=1; BIDUPSID=1F0227587C7DE38C985A29282BA65D3C; PSTM=1555164181; BDUSS=dOTDNyMENROURBSEY2UUFWUzFVZzJ1SC1ZM3V6MS1lSndkNDR-VEt0b0dqbU5lRVFBQUFBJCQAAAAAAAAAAAEAAADr11OO2aTAtsvC1tDSucz90-oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYBPF4GATxeUz; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=3; BDRCVFR[fb3VbsUruOn]=mk3SLVN4HKm; H_PS_PSSID=30971_1442_31123_21078_30901_30824_31085_22160; BDRCVFR[fBLL8ZbbiMm]=ddONZc2bo5mfAF9pywdpAqVuNqsus; __guid=177018279.2475572309495775000.1584594462077.4543; monitor_count=1",
            "Host": "site.baidu.com",
            "Pragma": "no-cache",
            "Referer": "https://www.baidu.com/link?url=3u6R-ggwSgPjdZ7sLKdVV5EKAY4sL8w5yJ06jeqqtQe&wd=&eqid=c5778c3e0000baf3000000055e72fe0c",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        },
        "callbalk": responseTest_default,
    },
]
HTTPS_TEST_LIST = [
    {
        "url": "https://www.baidu.com/",
        "header": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # "Cookie": "BAIDUID=1F0227587C7DE38C985A29282BA65D3C:FG=1; BIDUPSID=1F0227587C7DE38C985A29282BA65D3C; PSTM=1555164181; BDUSS=dOTDNyMENROURBSEY2UUFWUzFVZzJ1SC1ZM3V6MS1lSndkNDR-VEt0b0dqbU5lRVFBQUFBJCQAAAAAAAAAAAEAAADr11OO2aTAtsvC1tDSucz90-oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYBPF4GATxeUz; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ispeed_lsm=2; __guid=136081015.3054523526233476600.1584521570706.7397; COOKIE_SESSION=11558_0_9_5_2_4_1_0_9_4_1_0_53_0_56_0_1584539479_0_1584539423%7C9%232483674_29_1584516574%7C5; BD_HOME=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; BD_CK_SAM=1; PSINO=3; H_PS_PSSID=30971_1442_31123_21078_30901_30824_31085_22160; monitor_count=62",
            "Host": "www.baidu.com",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        },
        "callbalk": responseTest_default,
    },
    {
        "url": "https://www.hao123.com/",
        "header": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # "Cookie": "BAIDUID=38E53117388AEA8DA9AB47456B2B67FD:FG=1; BDUSS=VLdDh2eTZvVjh2VVlCRWtxOWhqSWxqWnZPTURFcFJGR2hjZH4xcHVSUlNDVjVlRVFBQUFBJCQAAAAAAAAAAAEAAADr11OO2aTAtsvC1tDSucz90-oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFJ8Nl5SfDZeRj; hz=0; s_ht_pageid=16; ft=1; v_pg=normal; __guid=35834534.3281635946426700300.1584601867623.4639; monitor_count=1; Hm_lvt_0703cfc0023d60b244e06b5cacfef877=1584601868; Hm_lpvt_0703cfc0023d60b244e06b5cacfef877=1584601868; hword=19; tnwhiteft=XzFYUBclcMPGIANCmytknWnBQaFYTzclnHR3PjmsnH6vrZY; __bsi=11403341384655543681_00_34_N_R_6_0303_c02f_Y",
            "Host": "www.hao123.com",
            "Pragma": "no-cache",
            "Referer": "https://www.baidu.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        },
        "callbalk": responseTest_default,
    },
    {
        "url": "https://www.csdn.net/",
        "header": {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            # "cookie": "uuid_tt_dd=10_28717561130-1554952762413-772741; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=1788*1*PC_VC!5744*1*qq_37782332!6525*1*10_28717561130-1554952762413-772741; smidV2=201810262351377bb0a607e67ea0f90e4f70a616ecdc21001d81ab7d4a9dca0; UN=qq_37782332; ADHOC_MEMBERSHIP_CLIENT_ID1.0=d8b354ef-5e84-4b3a-0435-1e6d74023e66; dc_session_id=10_1559914935151.501884; __guid=253029775.1916473904764723700.1581951943906.8542; UserName=qq_37782332; UserInfo=c609141e327e43e682a35895f548890b; UserToken=c609141e327e43e682a35895f548890b; UserNick=galanxc; AU=CF5; BT=1582720717335; p_uid=U000000; firstDie=1; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1584538573,1584539412,1584595715,1584601604; announcement=%257B%2522isLogin%2522%253Atrue%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fblog.csdn.net%252Fblogdevteam%252Farticle%252Fdetails%252F103603408%2522%252C%2522announcementCount%2522%253A0%252C%2522announcementExpire%2522%253A3600000%257D; c_adb=1; monitor_count=1; TY_SESSION_ID=fa89f4bf-f483-4c8f-9a4d-7b7d6a5bd004; c_ref=https%3A//blog.csdn.net/funnyPython/article/details/78444837; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1584601946; dc_tos=q7fioq",
            "pragma": "no-cache",
            "referer": "https://blog.csdn.net/funnyPython/article/details/78444837",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        },
        "callbalk": responseTest_default,
    },

]

ANONYMITY_TEST_LIST = {
    "HTTP": [
        {
            "url": "http://httpbin.org/get",
            "header": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                # "Cookie": "__guid=147723374.486925770027708200.1581480768812.5906; monitor_count=13",
                "Host": "httpbin.org",
                "Pragma": "no-cache",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            },
            "callbalk": getAnonymity_httpbin,
        },
    ],
    "HTTPS": [
        {
            "url": "https://httpbin.org/get",
            "header": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                # "Cookie": "__guid=147723374.486925770027708200.1581480768812.5906; monitor_count=1",
                "Host": "httpbin.org",
                "Pragma": "no-cache",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            },
            "callbalk": getAnonymity_httpbin,
        }
    ]
}

AREA_TEST_LIST = [
    {
        "url": "http://ip.tool.chinaz.com/{}",
        "useIP": True,
        "header": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "17",
            "Content-Type": "application/x-www-form-urlencoded",
            # "Cookie": "UM_distinctid=170b2f22b75548-0cc1c8d45db6d3-3c604504-1fa400-170b2f22b7656f; __guid=165978214.1877597054820343600.1584512517456.689; qHistory=aHR0cDovL2lwLnRvb2wuY2hpbmF6LmNvbS9pcGJhdGNoL19JUOaJuemHj+afpeivonxodHRwOi8vaXAudG9vbC5jaGluYXouY29tX0lQL0lQdjbmn6Xor6LvvIzmnI3liqHlmajlnLDlnYDmn6Xor6J8aHR0cDovL3Rvb2wuY2hpbmF6LmNvbV/nq5nplb/lt6Xlhbd8aHR0cDovL3BpbmcuY2hpbmF6LmNvbV9QaW5n5qOA5rWLfGh0dHA6Ly90b29sLmNoaW5hei5jb20vZG5zL19EbnPmn6Xor6I=; Hm_lvt_aecc9715b0f5d5f7f34fba48a3c511d6=1584539529; CNZZDATA5082706=cnzz_eid%3D1883741348-1584507927-null%26ntime%3D1584597517; monitor_count=10",
            "Host": "ip.tool.chinaz.com",
            "Origin": "http://ip.tool.chinaz.com",
            "Pragma": "no-cache",
            "Referer": "http://ip.tool.chinaz.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        },
        "callbalk": getArea_chinaz,
        # "method": "POST"
    }
]
