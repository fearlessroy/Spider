# -*- coding: utf-8 -*-

from scrapy import Spider
from scrapy.selector import Selector

from scrapy_spiders.items.loansite_items import LoansiteBusinessItems, LoansiteRainbowInfo, LoansitePaihuobaoInfo, \
    LoansiteYueuezhangInfo


class LoansiteBusinessInfoSpider(Spider):
    name = "loansite_business"
    start_urls = ['http://product.invest.ppdai.com/',
                  'http://invest.ppdai.com/product/rainbow',
                  'http://www.ppdai.com/', 'http://rise.invest.ppdai.com/#0'
                  ]

    def parse(self, response):
        html = response.text
        selector = Selector(text=html)
        if "product.invest" in response.url:
            paihuobaoinfo = LoansitePaihuobaoInfo()
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
            print(paihuobaoinfo)
        elif "rainbow" in response.url:
            loansiterainbowinfo = LoansiteRainbowInfo()
            loansiterainbowinfo['rainbow_invest_count'] = int(
                selector.xpath('//*[@id="r1"]/text()').extract_first().replace(',', ''))
            loansiterainbowinfo['rainbow_service_users'] = int(
                selector.xpath('//*[@id="r2"]/text()').extract_first().replace(',', ''))
            loansiterainbowinfo['rainbow_profit'] = int(
                selector.xpath('//*[@id="r3"]/text()').extract_first().replace(',', ''))
            print(loansiterainbowinfo)
        elif "rise" in response.url:
            loansiteyueyuezhang = LoansiteYueuezhangInfo()
            loansiteyueyuezhang['yueyuezhang_phase'] = selector.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/div/p/span[2]/text()').extract_first()
            loansiteyueyuezhang['annualized_rate_of_return'] = selector.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/div/div[1]/div[1]/p[1]/span[1]/text()').extract_first() + selector.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/div/div[1]/div[1]/p[1]/span[2]/text()').extract_first() + '%'
            loansiteyueyuezhang['invest_term'] = selector.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/div/div[1]/div[2]/p[1]/span/text()').extract_first() + '个月'
            loansiteyueyuezhang['total_amount'] = float(selector.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/div/div[1]/div[3]/p[1]/span/text()').extract_first())
            loansiteyueyuezhang['remain_amount_cast'] = float(
                selector.xpath('//*[@id="remainingAmount"]/text()').extract_first())
            loansiteyueyuezhang['purchase_limit'] = float(
                selector.xpath('//*[@id="formBuy"]/div/p[2]/span/b/text()').extract_first())
            loansiteyueyuezhang['aucumulated_investment'] = float(
                selector.xpath('/html/body/div[3]/div[1]/div[2]/div/div[1]/p/span/text()').extract_first().replace('¥',
                                                                                                                   ''))
            loansiteyueyuezhang['total_invest_users'] = int(
                selector.xpath('/html/body/div[3]/div[1]/div[2]/div/div[2]/p/span/text()').extract_first())
            loansiteyueyuezhang['aucumulated_profit'] = float(
                selector.xpath('/html/body/div[3]/div[1]/div[2]/div/div[3]/p/span/text()').extract_first().replace('¥',
                                                                                                                   ''))
            print(loansiteyueyuezhang)
        else:
            loansite_business_item = LoansiteBusinessItems()
            loansite_business_item['userscount'] = int(selector.xpath(
                '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[1]/p[1]/text()').extract_first().replace(',', ''))
            loansite_business_item['loanamount'] = int(selector.xpath(
                '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[2]/p[1]/text()').extract_first().replace(',', ''))
            loansite_business_item['dealvolume'] = int(float(selector.xpath(
                '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[2]/p[3]/text()').extract_first().replace(',',
                                                                                                             '').replace(
                '万', '')) * 10000)
            print(loansite_business_item)
