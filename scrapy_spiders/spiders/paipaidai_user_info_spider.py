# -*- coding: utf-8 -*-
import logging
import time
from scrapy import Selector

from scrapy_spiders.items.paipaidai_items import PaipaidaiUserInfo
from my_scrapy_redis.spiders import RedisSpider


class PaipaidaiUserinfoSpider(RedisSpider):
    name = 'paipaidai_user_info'
    redis_key = 'paiaidai:userinfo_urls'
    custom_settings = {
        'SCHEDULER': "scrapy.core.scheduler.Scheduler",
        'ITEM_PIPELINES': {
            'crawler.pipelines.paipaidai_pipeline.PaipaidaiBusinessPipeline': 400
        },
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.middlewares.middlewares.RandomUserAgent': 1,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
            'crawler.middlewares.middlewares.ProxyMiddleware': 100
        },
        'RETRY_TIMES': 3,
        'DOWNLOAD_DELAY': 5,
        'RANDOMIZE_DOWNLOAD_DELAY': True
    }

    logging.getLogger('scrapy').setLevel(logging.DEBUG)
    logging.getLogger("scrapy").propagate = True

    def __init__(self):
        super().__init__()

    def parse(self, response):
        html = response.text
        selector = Selector(text=html)
        userinfo = PaipaidaiUserInfo()
        userinfo['user_name'] = selector.xpath(
            '/html/body/div[4]/div[2]/div[1]/ul/li[1]/div/p/a/@title').extract_first()
        userinfo['user_sex'] = selector.xpath(
            '/html/body/div[4]/div[2]/div[1]/ul/li[3]/p[1]/span[1]/text()').extract_first().strip()
        userinfo['user_age'] = selector.xpath(
            '/html/body/div[4]/div[2]/div[1]/ul/li[3]/p[1]/span[2]/text()').extract_first().strip()
        userinfo['borrow_credit'] = selector.xpath(
            '/html/body/div[4]/div[2]/div[1]/ul/li[2]/p[1]/span/span/text()').extract_first()[:-2]
        userinfo['loan_credit'] = selector.xpath(
            '/html/body/div[4]/div[2]/div[1]/ul/li[2]/p[2]/span/span/text()').extract_first()[:-2]
        userinfo['identity'] = selector.xpath('/html/body/div[4]/div[2]/div[1]/ul/li[3]/p[2]/text()').extract_first()[
                               5:].strip()
        print(userinfo)
