from scrapy.utils.serialize import ScrapyJSONEncoder
from my_scrapy_redis.pipelines import RedisPipeline

default_serialize = ScrapyJSONEncoder().encode


class TmallCategoryPipeline(RedisPipeline):
    def __init__(self, server, serialize_func=default_serialize,
                 url_queue_key='%(spider)s:categoryurl_key', category_queue_key='%(spider)s:category_key'):
        super().__init__(server=server, serialize_func=serialize_func)
        self.url_queue_key = url_queue_key
        self.category_queue_key = category_queue_key

    def _process_item(self, item, spider):
        url = item['url']
        cat = item['cat']
        url_queue_key = self.spider_url_queue_key(spider)
        category_queue_key = self.spider_category_queue_key(spider)
        self.server.sadd(url_queue_key, url)
        self.server.sadd(category_queue_key, cat)
        return item

    def spider_url_queue_key(self, spider):
        return self.url_queue_key % {'spider': spider.name}

    def spider_category_queue_key(self, spider):
        return self.category_queue_key % {'spider': spider.name}
