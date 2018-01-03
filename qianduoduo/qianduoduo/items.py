# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


# params of investment
class InvestmentItem(Item):
    # 项目名称
    project_name = Field()
    # 项目状态
    project_status = Field()
    # 年化收益率
    annual_return = Field()
    # 借款金额
    loan_amount = Field()
    # 借款期限
    loan_life = Field()
    # 还款方式
    repayment_method = Field()
    # 二级链接
    secondary_href = Field()