"""
The module gets NBA schedules url from start url, scrapes schedules, and generates ics files.
"""

from scrapy import Spider, Request

from scrapy_spiders.items.nba_items import NBAScheduleItem


class NBAScheduleSpider(Spider):
    """
    This class is NBA scheduler Spider.
    """
    name = "nba_schedule"
    start_urls = ["http://g.hupu.com/nba/schedule"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.nba_pipeline.NBASchedulePipeline': 400
        }
    }

    def parse(self, response):
        parts = response.xpath(
            "/html/body/div[@id='allteamNba']/div[@class='players_left']/ul[@class='players_list']/li")
        for i in range(len(parts)):
            team_schedule_url = "http://g.hupu.com/{0}".format(
                parts[i].xpath(".//span[@class='team_name']/a/@href").extract_first())
            yield Request(url=team_schedule_url, callback=self.parse_team_schedule)

    def parse_team_schedule(self, response):  # do not mark as @staticmethod
        parts = response.xpath(
            "/html/body/div[@id='teamNba']/div[@class='players_right']/table[@class='players_table']/tbody/tr[@class='left']")
        for i in range(len(parts)):
            home_team_name = parts[i].xpath(".//td[@class='left'][1]/a/text()").extract_first()
            away_team_name = parts[i].xpath(".//td[@class='left'][1]/b/a/text()").extract_first()
            game_time = parts[i].xpath(".//td[@class='left'][4]/text()").extract_first()
            nba_schedule_item = NBAScheduleItem()
            nba_schedule_item["home_team_name"] = home_team_name
            nba_schedule_item["away_team_name"] = away_team_name
            nba_schedule_item["game_time"] = game_time
            nba_schedule_item["source_team_name"] = response.url.rsplit("/", 1)[-1]  # pass as ics filename
            yield nba_schedule_item
