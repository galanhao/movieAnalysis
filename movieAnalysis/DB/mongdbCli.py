import pymongo

from DB.conf import MongDB_URI, MongDB_DB_NAME, ProxyTaskSettingID, MongDB_SettingCol




class MongoDBCli:
    def __init__(self):
        self.client = pymongo.MongoClient(MongDB_URI)
        self.db = self.client[MongDB_DB_NAME]
        self.settingCol = self.db[MongDB_SettingCol]

    def getDBList(self):
        return self.client.list_database_names()


    def insertOne2Setting(self, data):
        ret = self.settingCol.insert_one(data)
        return ret
    def updateOne2Setting(self, oldD, newD):
        ret  = self.settingCol.update_one(oldD, newD)
        return ret
    def getProxySpiderConfig(self):
        ret = self.settingCol.find({"_id": ProxyTaskSettingID})
        spider_list  = [x["config"] for x in ret[0]["task"]["spiders"]]
        return spider_list
    def getProxySpider(self):
        ret = self.settingCol.find({"_id": ProxyTaskSettingID})[0]["task"]["spiders"]
        return ret
    def getOneSpiderConfigFromSpiderName(self, spider_name):
        spiders = self.getProxySpiderConfig()
        ret = None
        for spider in spiders:
            if spider["name"] == spider_name:
                ret = spider
                break
        return ret








tmp = {
    "_id": ProxyTaskSettingID,
    "task": {
        "spiders": [
            {
                "name": "快代理",
                "spiderName": "kuaidaili",
                "description":"",
                "startIndex": 1,
                "endIndex": 7,
                "config": {
                    "name": "kuaidaili",
                    "url": "https://www.kuaidaili.com/free/inha/{}/",
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

if __name__ == "__main__":
    db = MongoDBCli()
    # db.insertOne2Setting(tmp)
    # print(">>", db.getProxySpiderConfig())
    print(">>", db.getOneSpiderConfigFromSpiderName("kuaidaili1"))
