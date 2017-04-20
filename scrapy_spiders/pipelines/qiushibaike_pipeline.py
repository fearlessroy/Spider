from orm.models.qiushibaike import qiushibaike
from orm.models.base import DBSession


class QiushibaikePipeline(object):
    def __init__(self):
        self.session = DBSession()
        self.batch = []

    def process_item(self, item, spider):
        cinemaitem = qiushibaike(**item)
        self.batch.append(cinemaitem)

    def close_spider(self, spider):
        for i in self.batch:
            self.session.add(i)
        self.session.commit()
        self.session.close()
