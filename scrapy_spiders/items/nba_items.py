# -*- coding: utf-8 -*-

import scrapy


class NBAScheduleItem(scrapy.Item):
    home_team_name = scrapy.Field()
    away_team_name = scrapy.Field()
    game_time = scrapy.Field()
    source_team_name = scrapy.Field()
