from scrapy_spiders.pipelines.base_pipeline import BasePipeline
from orm.models.zhuanziban import ZhuanzibanCinema


class ZhuanzibanCinemaPipeline(BasePipeline):
    def __init__(self):
        super().__init__(batch_process_number=1, use_mysql=False,
                         jarvis_logger_filename="zhuanziban_cinema_pipeline.log")

    def process_item(self, item, spider):
        try:
            cinemaitem = ZhuanzibanCinema(**item)
            self.batch.append(cinemaitem)

        except Exception as e:
            self.jarvis_logger.exception(e=e)

