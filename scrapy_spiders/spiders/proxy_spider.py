# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy_spiders.items.proxy_items import ProxyItem
import redis


class ProxySpider(Spider):
    """
    It's the class to crawl IP address and port from xicidaili.com
    """
    name = 'proxy'
    allowed_domain = ['http://www.xicidaili.com/']
    start_urls = []
    for i in range(1, 3):
        url_com = 'http://www.xicidaili.com/nt/{0}'.format(i)
        start_urls.append(url_com)
    url_spe = 'http://www.xicidaili.com/nn/1'
    start_urls.append(url_spe)

    def __init__(self, *args, **kwargs):
        super(ProxySpider, self).__init__(*args, **kwargs)
        self.redis_key = 'proxy_ip'
        self.r = redis.Redis(host='127.0.0.1', port=6379, db=0)

    def parse(self, response):
        html = response.text
        selector = Selector(text=html)
        ip_group = selector.xpath('//*[@id="ip_list"]')
        for ip_info in ip_group:
            print(ip_info)
            for i in range(2, 102):
                item = ProxyItem()
                item['IP'] = ip_info.xpath('tbody/tr[{0}]/td[2]/text()'.format(
                    i)).extract_first()
                item['port'] = ip_info.xpath('tbody/tr[{0}]/td[3]/text()'.format(
                    i)).extract_first()
                proxy_url = item['IP'] + ":" + item['port']
                (self.r).sadd(self.redis_key, proxy_url)
                yield item
