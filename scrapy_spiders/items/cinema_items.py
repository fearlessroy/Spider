# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CinemaItem(scrapy.Item):
    date = scrapy.Field()
    cinema_company = scrapy.Field()
    daily_box_office = scrapy.Field()
    action_cutting = scrapy.Field()
    daily_viewers = scrapy.Field()
    counter_sales = scrapy.Field()
    counter_sales_percent = scrapy.Field()
    online_sales = scrapy.Field()
    online_sales_percent = scrapy.Field()

