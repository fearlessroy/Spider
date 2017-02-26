from scrapy_spiders.utils.db_operation import BaseDB
# from palmutil.logger_util import JarvisLogger


class BasePipeline(object):
    def __init__(self, batch_process_number=1, use_mysql=True, jarvis_logger_filename=""):
        self.batch = []
        self.batch_process_number = batch_process_number
        self.use_mysql = use_mysql
        # self.jarvis_logger = JarvisLogger(filename=jarvis_logger_filename)
        self.db_instance = BaseDB.from_config('config/env.cfg', use_mysql=self.use_mysql)

    def open_spider(self, spider):
        self.db_instance.connect_db()

    def insert_item(self, item):
        '''
        This method will insert item to data base
        Parameters
        ----------
        item: parse from spider

        Returns
        -------
        whatever is True or False it will return the item
        '''
        self.batch.append(item)
        if len(self.batch) >= self.batch_process_number:
            self.batch_insert_data(self.batch)
            self.batch = []
        return item

    def batch_insert_data(self, data):
        '''
        This method is default method to insert a batch of data
        Parameters
        ----------
        data: a batch of item

        Returns
        -------
        True or False
        '''
        return self.db_instance.batch_insert_data(data)

    def close_spider(self, spider):
        self.db_instance.batch_insert_data(self.batch)
        self.db_instance.close_db()
