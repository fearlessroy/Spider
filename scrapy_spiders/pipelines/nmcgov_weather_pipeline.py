import sys

from .base_pipeline import BasePipeline

reload(sys)
sys.setdefaultencoding('utf-8')


# class NmcgovWeatherPipeline(object):
#     def __init__(self):
#         self.connection = pymongo.MongoClient('127.0.0.1', 27017)
#         self.tdb = self.connection.foobar
#         self.post = self.tdb.weather
#         # self.file = open('weather_item.txt', 'wb')
#
#     def process_item(self, item, spider):
#         # line = json.dumps(dict(item), ensure_ascii=False)
#         # self.file.write(line)
#         self.post.insert(dict(item))
#         return item
#
#     def close_spider(self, spider):
#         # self.file.close()
#         self.connection.close()

class NmcgovWeatherPipeline(BasePipeline):
    def __init__(self):
        super(NmcgovWeatherPipeline, self).__init__(mongo_db='foobar', mongo_collection='weather')

    def process_item(self, item, spider):
        self.post.insert(dict(item))
        return item
