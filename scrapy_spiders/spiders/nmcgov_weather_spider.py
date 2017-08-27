# -*- coding = utf-8 -*-
import traceback

from scrapy import Spider, Request

from ..items.nmcgov_weather_info_items import NmcgovWeatherSpiderItem

'''
crawl weather info from http://www.nmc.gov.cn/(zhongyangqixiangtai),
the websites like:
        http://www.nmc.gov.cn/f/rest/province           : return province,autonomous region and municipalities' code
        http://www.nmc.gov.cn/f/rest/province/AJS       : find the city and city code for the corresponding provinces
        http://www.nmc.gov.cn/f/rest/tempchart/54620    : return one city's weather two weaker before and later by city_code
        http://www.nmc.gov.cn/f/rest/real/54616         : the day weather by city_code
'''


class NmcgovWeatherSpider(Spider):
    name = "nmcgov_weather"
    start_urls = ['http://www.nmc.gov.cn/f/rest/province']
    custom_settings = {
        'SCHEDULER': "scrapy.core.scheduler.Scheduler",
        'ITEM_PIPELINES': {
            'weather_spider.pipelines.nmcgov_weather_pipeline.NmcgovWeatherPipeline': 400
        },
    }

    def parse(self, response):
        provinces_code = []
        req_list = eval(response.text)
        for dict_item in req_list:
            provinces_code.append(dict_item['code'])
        # provinces_code = ['AHN']
        for code in provinces_code:
            if code:
                yield Request(self.get_city_info(code), callback=self.parse_city)

    def parse_city(self, response):
        html = response.text
        city_list = eval(html)
        for city_info in city_list:
            if city_info['url']:
                yield Request(self.get_city_today_weather(city_info['code']), callback=self.parse_city_weather)

    def parse_city_weather(self, response):
        try:
            html = response.text
            if html:
                city_weather = eval(html)
                weather_item = NmcgovWeatherSpiderItem()
                weather_info = []
                if city_weather["weather"]:
                    weather_info.append(city_weather["weather"])
                if city_weather['wind']:
                    weather_info.append(city_weather['wind'])
                weather_item['city_name'] = city_weather['station']['province'] + city_weather['station']['city']
                weather_item['city_code'] = city_weather['station']['code']
                weather_item['city_today_weather'] = weather_info
                weather_item['weather_publish_time'] = city_weather['publish_time']
                if city_weather['warn']['alert'] != '9999':  # magic number
                    weather_item['weather_warning'] = ','.join((
                                                                   city_weather['warn']['alert'] + ',' +
                                                                   city_weather['warn'][
                                                                       'issuecontent']).replace('\n', '').split())
                else:
                    weather_item['weather_warning'] = ''
                yield weather_item
        except:
            traceback.print_exc()

    @staticmethod
    def get_city_info(provice_code):
        return "http://www.nmc.gov.cn/f/rest/province/" + provice_code

    @staticmethod
    def get_city_today_weather(city_code):
        return "http://www.nmc.gov.cn/f/rest/real/" + city_code
