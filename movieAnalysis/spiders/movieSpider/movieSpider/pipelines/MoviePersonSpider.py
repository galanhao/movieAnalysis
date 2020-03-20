from movieManager.models import Person, Identity
from spiders.movieSpider.movieSpider.spiders.maoYan_person import MaoyanPersonSpider


class Pipeline(object):
    def process_item(self, item, spider):
        # print(spider.name, MaoyanPersonSpider.name)
        if spider.name == MaoyanPersonSpider.name:
            # print("jinru ")
            person = Person.objects.filter(user_id=item["user_id"]).first()
            if person:
                # print("找到Person")
                person.name = item["name"]
                person.foreign_name = item["foreign_name"]
                person.birth_place = item["birth_place"]
                person.national = item["national"]
                person.nationality = item["nationality"]
                person.introduce = item["introduce"]
                person.gender = 0
                if item["gender"] == "男":
                    person.gender= 1
                elif item["gender"] == "女":
                    person.gender = 2
                if item["identity"]:
                    for ciden in item["identity"]:
                        cidenTmp = Identity.objects.filter(name=ciden).first()
                        if not cidenTmp:
                            cidenTmp = Identity.objects.create(name=ciden)
                        perIdenTmp = person.identity.filter(name=ciden).first()
                        if not perIdenTmp:
                            person.identity.add(cidenTmp)
                person.save()
        return item