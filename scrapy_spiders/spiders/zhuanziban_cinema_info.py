# -*- coding:utf-8-*-
import datetime

import scrapy
from scrapy.selector import Selector

from scrapy_spiders.items import ZhuanzibanCinemaItem


class ZhuanzibanCinemaSpier(scrapy.Spider):
    name = 'zhuanziban_cinema'
    allowed_domains = ['http://111.205.151.7/cine_groups/']
    # start_urls = ['http://111.205.151.7/cine_groups/{0}-{1}-{2}'.format(datetime.datetime.now().year,
    #                                                                     datetime.datetime.now().month,
    #                                                                     datetime.datetime.now().day)]
    start_urls=['http://111.205.151.7/cine_groups/2017-01-01']
    # custom_settings = {
    #     'SCHEDULER': "scrapy.core.scheduler.Scheduler",
    #     'ITEM_PIPELINES': {
    #         'crawler.pipelines.zhuanziban_info_redshift_pipeline.ZhuanzibanCinemaPipeline': 400
    #     }
    # }

    def parse(self, response):
        html = response.body.decode().encode("utf-8")
        selector = Selector(text=html)
        movie_group = selector.xpath('//html/body/div')
        for movie_item in movie_group:
            for i in range(1, 11):  # Information in a table with ten rows.
                item = ZhuanzibanCinemaItem()
                item['date'] = movie_group.xpath(
                    'div[1]/header/a[2]/span[1]/text()').extract_first()
                item['cinema_company'] = movie_item.xpath('table/tbody/tr[{0}]/td[1]/text()'.format(i)).extract_first()
                item['daily_box_office'] = int(movie_item.xpath(
                    'table/tbody/tr[{0}]/td[2]/text()'.format(i)).extract_first().replace(',', ''))
                item['action_cutting'] = int(movie_item.xpath(
                    'table/tbody/tr[{0}]/td[3]/text()'.format(i)).extract_first().replace(',', '').replace(',',
                                                                                                           '').replace(
                    '场', ''))
                item['daily_viewers'] = int(
                    movie_item.xpath('table/tbody/tr[{0}]/td[3]/i/text()'.format(i)).extract_first().replace(',', ''))
                item['counter_sales'] = int(
                    movie_item.xpath('table/tbody/tr[{0}]/td[4]/text()'.format(i)).extract_first().replace(',', ''))
                item['counter_sales_percent'] = movie_item.xpath(
                    'table/tbody/tr[{0}]/td[4]/i/text()'.format(i)).extract_first()
                item['online_sales'] = int(
                    movie_item.xpath('table/tbody/tr[{0}]/td[5]/text()'.format(i)).extract_first().replace(',', ''))
                item['online_sales_percent'] = movie_item.xpath(
                    'table/tbody/tr[{0}]/td[5]/i/text()'.format(i)).extract_first()
                # yield item
                print(item)