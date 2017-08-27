import pymongo


class NmcgovWeatherPipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient('127.0.0.1', 27017)
        self.tdb = self.connection.nmc_weather
        self.post = self.tdb.weather
        # self.file = open('weather_item.txt', 'wb')

    def process_item(self, item, spider):
        # line = json.dumps(dict(item), ensure_ascii=False)
        # self.file.write(line)
        self.post.insert(dict(item))
        return item

    def close_spider(self, spider):
        # self.file.close()
        self.connection.close()