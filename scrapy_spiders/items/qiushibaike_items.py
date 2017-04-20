import scrapy


class QiushibaikeItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    like_count = scrapy.Field()
    comment_count = scrapy.Field()
    date = scrapy.Field()
    created_date = scrapy.Field()
    user_id = scrapy.Field()