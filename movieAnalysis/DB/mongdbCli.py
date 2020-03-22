import pymongo

from DB.conf import MongDB_URI, MongDB_DB_NAME, ProxyTaskSettingID, MongDB_SettingCol
from movieAnalysis.settings import logger


class MongoDBCli:
    def __init__(self):
        self.client = pymongo.MongoClient(MongDB_URI)
        self.db = self.client[MongDB_DB_NAME]
        self.settingCol = self.db[MongDB_SettingCol]

        self.spider_flag = "spider_info"

    def getDBList(self):
        return self.client.list_database_names()

    def __checkSpiderInfo(self, data):
        spider_config = data.get("config", False)
        if spider_config == False:
            return False
        spider_name = spider_config.get("name", False)
        if spider_name == False:
            return False

        return True
    def __insertSpiderInfo(self, data):
        logger.info("__insertSpiderInfo 传入 {}".format(data))
        try:
            insert_data = {
                "flag": self.spider_flag,
                "spider_name": data["config"]["name"],
                "content": data
            }
            logger.info("__insertSpiderInfo {}".format(insert_data))
            ret = self.settingCol.insert_one(insert_data)
            # print("insert", insert_data)
            # ret.inserted_id
            return ret
        except BaseException as e:
            logger.error("__insertSpiderInfo error {}".format(e))
            pass
        return None

    def __deleteSpiderInfo(self, data):
        try:
            delete_data = {
                "flag": self.spider_flag,
                "spider_name": data["config"]["name"],
                "content": data
            }
            r = self.settingCol.remove(delete_data)
            logger.debug("{}的remove结果{}".format(data, r))
        except BaseException as e:
            logger.error("__deleteSpiderInfo error %s"%e)


    def setOneSpider(self, data):
        # 检查传入的data
        # print("setOneSpider 传入", data)
        if not self.__checkSpiderInfo(data):
            return None
        # print({"flag": self.spider_flag, "spider_name": data["config"]["name"]})
        find_spider = self.settingCol.find_one({"flag": self.spider_flag, "spider_name": data["config"]["name"]})
        # print(find_spider)
        if find_spider != None:
            # print(find_spider)
            logger.debug("开始删除已存在的spider {}".format(find_spider))
            self.__deleteSpiderInfo(find_spider["content"])
        return self.__insertSpiderInfo(data).inserted_id


    def getOneSpiderBySpiderName(self, spider_name):
        find_spider = self.settingCol.find_one({"flag": self.spider_flag, "spider_name": spider_name})
        return find_spider

    def getOneSpiderFromSpiderName(self, spider_name):
        find_spider = self.settingCol.find_one({"flag": self.spider_flag, "spider_name": spider_name})
        if find_spider == None:
            return None
        return find_spider["content"]


    def getAllSpider(self):
        find_spiders = list(self.settingCol.find({"flag": self.spider_flag}))
        return [x["content"] for x in find_spiders]

    def getAllSpiderConfig(self):
        find_spiders = list(self.settingCol.find({"flag": self.spider_flag}))
        ret = [x["content"]["config"] for x in find_spiders]
        return ret











tmp = {
    "_id": ProxyTaskSettingID,
    "task": {
        "spiders": [
            {
                "name": "快代理",
                "description":"",
                "startIndex": 1,
                "endIndex": 7,
                "config": {
                    "name": "kuaidaili",
                    "url": "https://www.kuaidaili.com/free/inha/{}/",
                    "useRange": True,
                    "header": {
                        "Host": "www.kuaidaili.com",
                        "Upgrade-Insecure-Requests": "1",
                        'Connection': 'keep-alive',
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "zh-CN,zh;q=0.9"
                    },
                    "oneLine": ["//tr", ],
                    "ip": "td[1]/text()",
                    "port": "td[2]/text()"
                },
            }
        ],
        "others": [

        ]
    }
}

spider_tmp = {
                "name": "快代理",
                "description":"",
                "startIndex": 1,
                "endIndex": 9,
                "config": {
                    "name": "kuaidaili",
                    "url": "https://www.kuaidaili.com/free/inha/{}/",
                    "useRange": True,
                    "header": {
                        "Host": "www.kuaidaili.com",
                        "Upgrade-Insecure-Requests": "1",
                        'Connection': 'keep-alive',
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "zh-CN,zh;q=0.9"
                    },
                    "oneLine": ["//tr", ],
                    "ip": "td[1]/text()",
                    "port": "td[2]/text()"
                },
            }


if __name__ == "__main__":
    db = MongoDBCli()

    print(db.setOneSpider(spider_tmp))
    print(db.getAllSpider())


    # db.insertOne2Setting(tmp)
    # print(">>", db.getProxySpiderConfig())
    # print(">>", db.getOneSpiderConfigFromSpiderName("kuaidaili"))
