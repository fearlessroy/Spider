# -*- coding: utf-8 -*-
import scrapy

"""
annualized_rate_of_return:预期年化收益率
invest_term：投资期限
aucumulated_investment：累计投资总额
aucumulated_profit：累计已赚
"""


class LoansiteBaseItem(scrapy.Item):
    crawl_date = scrapy.Field()
    process_date = scrapy.Field()


class LoansiteBusinessItems(LoansiteBaseItem):
    userscount = scrapy.Field()
    loanamount = scrapy.Field()
    dealvolume = scrapy.Field()


class LoansiteRainbowInfo(LoansiteBaseItem):
    rainbow_invest_count = scrapy.Field()
    rainbow_service_users = scrapy.Field()
    rainbow_profit = scrapy.Field()


class LoansiteYueuezhangInfo(LoansiteBaseItem):
    yueyuezhang_phase = scrapy.Field()
    annualized_rate_of_return = scrapy.Field()
    invest_term = scrapy.Field()
    total_amount = scrapy.Field()
    remain_amount_cast = scrapy.Field()
    purchase_limit = scrapy.Field()
    aucumulated_investment = scrapy.Field()
    total_invest_users = scrapy.Field()
    aucumulated_profit = scrapy.Field()


class LoansitePaihuobaoInfo(LoansiteBaseItem):
    annualized_rate_of_return = scrapy.Field()
    aucumulated_investment = scrapy.Field()
    total_invest_users = scrapy.Field()
    aucumulated_profit = scrapy.Field()


class LoansiteRainbowItem(LoansiteBaseItem):
    plan_id = scrapy.Field()
    annualized_rate_of_return = scrapy.Field()
    invest_term = scrapy.Field()
    total_amount = scrapy.Field()
    remain_amount_cast = scrapy.Field()
    purchase_limit = scrapy.Field()
    start_purchase_date = scrapy.Field()
    income_date = scrapy.Field()
    source_url = scrapy.Field()


class LoansiteLinkItem(LoansiteBaseItem):
    user_info = scrapy.Field()
    loan_info = scrapy.Field()


class LoansiteUserInfo(LoansiteBaseItem):
    user_name = scrapy.Field()
    user_sex = scrapy.Field()
    user_age = scrapy.Field()
    borrow_credit = scrapy.Field()
    loan_credit = scrapy.Field()
    identity = scrapy.Field()


class LoansiteLoanInfo(LoansiteBaseItem):
    user_name = scrapy.Field()
    successful_times = scrapy.Field()
    failed_times = scrapy.Field()
    credit_rank = scrapy.Field()
