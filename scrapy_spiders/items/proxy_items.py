# -*- coding: utf-8 -*-

import scrapy


class ProxyItem(scrapy.Item):
    IP = scrapy.Field()
    port = scrapy.Field()
