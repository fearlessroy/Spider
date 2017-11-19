# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import random
import time
from scrapy_spiders.items.qiushibaike_items import QiushibaikeItem
from bs4 import BeautifulSoup


class QiushibaikeSpier(scrapy.Spider):
    name = 'qiushibaike'
    allowed_domains = ['https://www.qiushibaike.com/']
    start_urls = ['https://www.qiushibaike.com/']

    custom_settings = {
        'SCHEDULER': "scrapy.core.scheduler.Scheduler",
        'ITEM_PIPELINES': {
            'scrapy_spiders.pipelines.qiushibaike_pipeline.QiushibaikePipeline': 400
        }
    }

    def parse(self, response):
        html = response.body.decode().encode("utf-8")
        # selector = Selector(text=html)
        soup = BeautifulSoup(html)
        for a in soup.find_all('a', target="_blank"):
            if '/article/' in a['href']:
                for child in a.children:
                    if child.name == 'div':
                        item = QiushibaikeItem()
                        item['link'] = "https://www.qiushibaike.com{}".format(a['href'])
                        # print(child.span.text[0:8])
                        item['title'] = child.span.text[0:8]
                        item['image'] = "http://images.nowcoder.com/head/{}t.png".format(random.randint(1, 1000))
                        item['like_count'] = 0
                        item['comment_count'] = 0
                        item['created_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        item['user_id'] = 0
                        if item['title'] and item['link']:
                            yield item
