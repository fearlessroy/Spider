import scrapy


class NmcgovWeatherSpiderItem(scrapy.Item):
    city_name = scrapy.Field()
    city_code = scrapy.Field()
    city_today_weather = scrapy.Field()
    weather_publish_time = scrapy.Field()
    weather_warning = scrapy.Field()
