# -*- coding: utf-8 -*-
import logging
import re

from scrapy import Spider, Selector, Request
from bs4 import BeautifulSoup
from scrapy_spiders.items.paipaidai_items import PaipaidaiRainbowItem



class PaipaidaiRainbowPlanSpider(Spider):
    name = 'paipaidai_rainbow_plan'
    start_urls = ['http://invest.ppdai.com/product/rainbow']
    custom_settings = {
        'SCHEDULER': "scrapy.core.scheduler.Scheduler",
    }

    logging.getLogger('scrapy').setLevel(logging.DEBUG)
    logging.getLogger("scrapy").propagate = True

    def __init__(self):
        super().__init__()

    def parse(self, response):
        if response.status == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            tags = soup.find_all('a')
            for tag in tags:
                link = tag.get('href')
                if link and '/product/info' in link:
                    url = '{0}{1}'.format('http://invest.ppdai.com', link.replace(';', '&'))
                    yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        if response.status == 200:
            html = response.text
            selector = Selector(text=html)
            rainbowitem = PaipaidaiRainbowItem()
            rainbowitem['plan_id'] = int(re.search(r'id=(\d+)', response.url).group(1))
            rainbowitem['annualized_rate_of_return'] = selector.xpath('//*[@id="theRate"]/text()').extract_first() + '%'
            rainbowitem['invest_term'] = selector.xpath('//*[@id="theMonth"]/text()').extract_first() + '个月'
            rainbowitem['total_amount'] = selector.xpath(
                '//*[@id="content_nav"]/div[1]/div[2]/div/div/div[2]/div[1]/span[3]/p/i/text()').extract_first().replace(
                ',', '')
            rainbowitem['remain_amount_cast'] = int(
                selector.xpath('//*[@id="remainingAmount"]/text()').extract_first().replace(
                    '¥', '').replace(',', ''))
            rainbowitem['purchase_limit'] = int(selector.xpath(
                '//*[@id="content_nav"]/div[1]/div[2]/div/div/div[3]/ul/li[2]/span[2]/text()').extract_first().replace(
                ',',
                '').replace(
                '¥', '').replace('元', ''))
            rainbowitem['start_purchase_date'] = selector.xpath(
                '//*[@id="content_nav"]/div[1]/div[2]/div/div/div[2]/div[2]/span[2]/p/text()').extract_first().replace(
                '开放购买时间：', '').strip()
            rainbowitem['income_date'] = selector.xpath(
                '//*[@id="content_nav"]/div[1]/div[2]/div/div/div[2]/div[2]/span[2]/p/i/text()').extract_first().replace(
                '投资收益日：', '')
            rainbowitem['source_url'] = response.url
            print(rainbowitem)
