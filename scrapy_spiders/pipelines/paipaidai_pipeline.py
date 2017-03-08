from scrapy.utils.serialize import ScrapyJSONEncoder
from my_scrapy_redis.pipelines import RedisPipeline
from orm.models.paipaidai import PaipaidaiBusinessInfo, PaipaidaiPaihuobao, PaipaidaiRainbowInfo, PaipaidaiYueyuezhang, \
    PaipaidaiRainbowPlan, PaipaidaiUserinfo, PaipaidaiLoanInfo

default_serialize = ScrapyJSONEncoder().encode


class PaipaidaiBusinessPipeline():
    def __init__(self):
        super().__init__(batch_process_number=10, use_mysql=True,
                         jarvis_logger_filename="paipaidai_business_pipeline.log")

    def process_item(self, item, spider):
        if "rainbow_invest_count" in item:
            rainbowinfo = PaipaidaiRainbowInfo(**item)
            self.batch.append(rainbowinfo)
        elif "userscount" in item:
            paipaidai_businsessinfo_item = PaipaidaiBusinessInfo(**item)
            self.batch.append(paipaidai_businsessinfo_item)
        elif "yueyuezhang_phase" in item:
            yueyuezhang_item = PaipaidaiYueyuezhang(**item)
            self.batch.append(yueyuezhang_item)
        elif "borrow_credit" in item:
            userinfo = PaipaidaiUserinfo(**item)
            self.batch.append(userinfo)
            self.db_instance.batch_insert_data(self.batch)
        elif "successful_times" in item:
            loaninfo = PaipaidaiLoanInfo(**item)
            self.batch.append(loaninfo)
            self.db_instance.batch_insert_data(self.batch)
        else:
            paihuobao_item = PaipaidaiPaihuobao(**item)
            self.batch.append(paihuobao_item)


class PaipaidaiRainbowPlanPipeline(BasePipeline):
    def __init__(self):
        super().__init__(batch_process_number=10, use_mysql=True,
                         jarvis_logger_filename="paipaidai_rainbowplan_pipeline.log")

    def process_item(self, item, spider):
        rainbowplan = PaipaidaiRainbowPlan(**item)
        self.batch.append(rainbowplan)
        if len(self.batch) >= self.batch_process_number:
            self.db_instance.batch_insert_data(self.batch)
            self.jarvis_logger.info(msg="Insert {} items".format(len(self.batch)))
            self.batch.clear()
        return rainbowplan


class PaipaidaiLinkPipeline(RedisPipeline):
    def __init__(self, server, serialize_func=default_serialize):
        super().__init__(server=server, serialize_func=serialize_func)
        self.userinfo_url_key = 'paiaidai:userinfo_urls'
        self.loaninfo_url_key = 'paipaidai:loaninfo_urls'

    def process_item(self, item, spider):
        loan_info = item['loan_info']
        if item['user_info']:  # parse different start_urls will return items with different length
            user_info = item['user_info']
            self.server.sadd(self.userinfo_url_key, user_info)
        self.server.sadd(self.loaninfo_url_key, loan_info)
        return item
