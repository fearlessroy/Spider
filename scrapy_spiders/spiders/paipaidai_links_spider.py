# -*- coding: utf-8 -*-
import logging
import re
import time

from scrapy import Spider, Request, Selector

from scrapy_spiders.items.paipaidai_items import PaipaidaiLinkItem


class PaipaipaiLinksSpider(Spider):
    name = 'paipaidai_links'
    start_urls = [
        'http://invest.ppdai.com/loan/listnew?LoanCategoryId=8&SortType=0&PageIndex=1&MinAmount=0&MaxAmount=0',
        'http://invest.ppdai.com/loan/listnew?LoanCategoryId=5&SortType=0&PageIndex=1&MinAmount=0&MaxAmount=0',
        'http://invest.ppdai.com/loan/listnew?LoanCategoryId=4&SortType=0&PageIndex=1&MinAmount=0&MaxAmount=0',
        'http://invest.ppdai.com/AllDebtList/DebtList?monthgroup=&nodelayrate=0&CType=1&SortType=0&levels=%2C&LastDueDays=&IsShowMore=0&MinAmount=-1&MaxAmount=-1',
        'http://invest.ppdai.com/AllDebtList/DebtList?monthgroup=&nodelayrate=0&CType=2&SortType=0&levels=%2C&LastDueDays=&IsShowMore=0&MinAmount=-1&MaxAmount=-1',
        'http://invest.ppdai.com/AllDebtList/DebtList?monthgroup=&nodelayrate=0&CType=3&SortType=0&levels=%2C&LastDueDays=&IsShowMore=0&MinAmount=-1&MaxAmount=-1'
    ]

    custom_settings = {
        'SCHEDULER': "scrapy.core.scheduler.Scheduler",
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.middlewares.middlewares.RandomUserAgent': 1,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
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
        try:
            html = response.text
            selector = Selector(text=html)
            is_empty = selector.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div[2]/h2/text()').extract_first()
            is_page = re.search(r'共(.*?)页', html)
            if 'LoanCategoryId' in response.url and not is_empty:
                if is_page:
                    total_page = int(is_page.group(1))
                    for i in range(1, total_page + 1):
                        url = 'http://invest.ppdai.com/loan/listnew?LoanCategoryId=8&SortType=0&&MinAmount=0&MaxAmount=0&PageIndex={0}'.format(
                            i)
                        time.sleep(5)
                        yield Request(url=url, callback=self.parse_loan)
                else:
                    yield Request(url=response.url, callback=self.parse_loan)
            elif 'DebtList' in response.url and not is_empty:
                if is_page:
                    total_page = int(is_page.group(1))
                    for i in range(1, total_page + 1):
                        url = 'http://invest.ppdai.com/AllDebtList/DebtList?MinAmount=-1&MaxAmount=-1&NoDelayRate=0&SortType=0&CType=1&PageIndex={0}'.format(
                            i)
                        time.sleep(5)
                        yield Request(url=url, callback=self.parse_deb)
                else:
                    yield Request(url=response.url, callback=self.parse_deb)
        except Exception as e:
            self.jarvis_logger.exception(e=e)

    def parse_loan(self, response):
        for item in response.css('ol.clearfix'):
            paipaidai_links = PaipaidaiLinkItem()
            paipaidai_links['user_info'] = item.xpath('li/div[2]/p/a/@href').extract_first()
            paipaidai_links['loan_info'] = item.xpath('li/div[2]/a/@href').extract_first()
            yield paipaidai_links

    def parse_deb(self, response):
        for item in response.css('li.subli '):
            paipaidai_links = PaipaidaiLinkItem()
            paipaidai_links['user_info'] = ''
            paipaidai_links['loan_info'] = 'http://invest.ppdai.com' + item.xpath('div/a/@href').extract_first()
            yield paipaidai_links
