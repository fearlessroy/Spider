"""
This module handles tmall database operations.
"""
from palmutil.db_operation import BaseDB
from orm.models.tmall import TmallProductInfo, TmallSalesInfo


class TmallDB(BaseDB):
    def batch_insert_prod(self, items):
        try:
            data = [TmallProductInfo(**{key: item[key] for key in TmallProductInfo.keys}) for item in items]
            return self.batch_insert_data(data)
        except Exception as e:
            self.jarvis_logger.exception(e=e)

    def batch_insert_sales(self, items):
        try:
            data = [TmallSalesInfo(**{key: item[key] for key in TmallSalesInfo.keys}) for item in items]
            return self.batch_insert_data(data)
        except Exception as e:
            self.jarvis_logger.exception(e=e)

    def is_product_existed(self, pk):
        try:
            existed = self.session.query(TmallProductInfo.sku_id).filter_by(sku_id=pk).count()
            return existed > 0
        except Exception as e:
            self.jarvis_logger.exception(e=e)
            return False
