from crawler.pipelines.base_pipeline import BasePipeline
from orm.models.tmall import TmallProductInfo


class TmallProductPipeline(BasePipeline):
    def __init__(self):
        super().__init__(batch_process_number=100, use_mysql=True, jarvis_logger_filename="tmall_product_pipeline.log")

    def process_item(self, item, spider):
        tmall_product_info = TmallProductInfo(**item)
        self.batch.append(tmall_product_info)
        if len(self.batch) >= self.batch_process_number:
            self.db_instance.batch_insert_data(self.batch)
            self.batch.clear()
        return tmall_product_info
