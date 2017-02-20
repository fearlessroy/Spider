# -*- coding: utf-8 -*-

from scrapy import Spider
from scrapy.selector import Selector

from scrapy_spiders.items.paipaidai_items import PaipaidaiBusinessItems, PaipaidaiRainbowInfo, PaipaidaiPaihuobaoInfo, \
    PaipaidaiYueuezhangInfo


# from palmutil.time_util import get_current_timestamp_str


class PaipaidaiBusinessInfoSpider(Spider):
    name = "paipaidai_business"
    start_urls = ['http://product.invest.ppdai.com/', 'http://invest.ppdai.com/product/rainbow',
                  'http://www.ppdai.com/', 'http://rise.invest.ppdai.com/#0']

    #
    # custom_settings = {
    #     'SCHEDULER': "scrapy.core.scheduler.Scheduler",
    #     'ITEM_PIPELINES': {
    #         'crawler.pipelines.paipaidai_pipeline.PaipaidaiBusinessPipeline': 400
    #     }
    # }

    def parse(self, response):
        # today = get_current_timestamp_str("Asia/Shanghai")
        html = response.text
        selector = Selector(text=html)
        if "product.invest" in response.url:
            paihuobaoinfo = PaipaidaiPaihuobaoInfo()
            paihuobaoinfo['annualized_rate_of_return'] = selector.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/div[1]/p[3]/text()').extract_first()
            paihuobaoinfo['aucumulated_investment'] = int(
                selector.xpath('/html/body/div[3]/div[1]/div[2]/div/div[1]/p/span/text()').extract_first().replace('¥',
                                                                                                                   '').replace(
                    ',', '').strip())
            paihuobaoinfo['total_invest_users'] = int(
                selector.xpath('/html/body/div[3]/div[1]/div[2]/div/div[2]/p/span/text()').extract_first().strip())
            paihuobaoinfo['aucumulated_profit'] = int(
                selector.xpath('/html/body/div[3]/div[1]/div[2]/div/div[3]/p/span/text()').extract_first().replace('¥',
                                                                                                                   '').replace(
                    ',', '').strip())
            # paihuobaoinfo['crawl_date'] = today
            # yield paihuobaoinfo
            print(paihuobaoinfo)
        elif "rainbow" in response.url:
            paipaidairainbowinfo = PaipaidaiRainbowInfo()
            paipaidairainbowinfo['rainbow_invest_count'] = int(
                selector.xpath('//*[@id="r1"]/text()').extract_first().replace(',', ''))
            paipaidairainbowinfo['rainbow_service_users'] = int(
                selector.xpath('//*[@id="r2"]/text()').extract_first().replace(',', ''))
            paipaidairainbowinfo['rainbow_profit'] = int(
                selector.xpath('//*[@id="r3"]/text()').extract_first().replace(',', ''))
            # paipaidairainbowinfo['crawl_date'] = today
            # yield paipaidairainbowinfo
            print(paipaidairainbowinfo)
        elif "rise" in response.url:
            paipaidaiyueyuezhang = PaipaidaiYueuezhangInfo()
            paipaidaiyueyuezhang['yueyuezhang_phase'] = selector.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/div/p/span[2]/text()').extract_first()
            paipaidaiyueyuezhang['annualized_rate_of_return'] = selector.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/div/div[1]/div[1]/p[1]/span[1]/text()').extract_first() + selector.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/div/div[1]/div[1]/p[1]/span[2]/text()').extract_first() + '%'
            paipaidaiyueyuezhang['invest_term'] = selector.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/div/div[1]/div[2]/p[1]/span/text()').extract_first() + '个月'
            paipaidaiyueyuezhang['total_amount'] = float(selector.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/div/div[1]/div[3]/p[1]/span/text()').extract_first())
            paipaidaiyueyuezhang['remain_amount_cast'] = float(
                selector.xpath('//*[@id="remainingAmount"]/text()').extract_first())
            paipaidaiyueyuezhang['purchase_limit'] = float(
                selector.xpath('//*[@id="formBuy"]/div/p[2]/span/b/text()').extract_first())
            paipaidaiyueyuezhang['aucumulated_investment'] = float(
                selector.xpath('/html/body/div[3]/div[1]/div[2]/div/div[1]/p/span/text()').extract_first().replace('¥',
                                                                                                                   ''))
            paipaidaiyueyuezhang['total_invest_users'] = int(
                selector.xpath('/html/body/div[3]/div[1]/div[2]/div/div[2]/p/span/text()').extract_first())
            paipaidaiyueyuezhang['aucumulated_profit'] = float(
                selector.xpath('/html/body/div[3]/div[1]/div[2]/div/div[3]/p/span/text()').extract_first().replace('¥',
                                                                                                                   ''))
            # paipaidaiyueyuezhang['crawl_date'] = today
            # yield paipaidaiyueyuezhang
            print(paipaidaiyueyuezhang)
        else:
            paipaidai_business_item = PaipaidaiBusinessItems()
            paipaidai_business_item['userscount'] = int(selector.xpath(
                '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[1]/p[1]/text()').extract_first().replace(',', ''))
            paipaidai_business_item['loanamount'] = int(selector.xpath(
                '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[2]/p[1]/text()').extract_first().replace(',', ''))
            paipaidai_business_item['dealvolume'] = int(float(selector.xpath(
                '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[2]/p[3]/text()').extract_first().replace(',',
                                                                                                             '').replace(
                '万', '')) * 10000)
            # paipaidai_business_item['crawl_date'] = today
            # yield paipaidai_business_item
            print(paipaidai_business_item)
