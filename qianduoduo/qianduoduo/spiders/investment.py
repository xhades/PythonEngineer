#! /usr/bin/env python
# -*-coding:utf-8-*-
__author__ = 'dahv'

import scrapy
from scrapy.spiders import CrawlSpider
import logging
import re
from scrapy.selector import Selector
from qianduoduo.items import InvestmentItem

class InvestmentSpider(CrawlSpider):
    name = 'invest'

    custom_settings = {'ITEM_PIPELINES': {'qianduoduo.pipelines.QianduoduoPipeline':300}}

    def __init__(self):
        super(InvestmentSpider, self).__init__()
        self.allowed_domains = ['http://d.com.cn/']
        self.start_urls = ['http://d.com.cn/lend-0-0-0-1.html']
        self.last_page_xpath = "//div[@id='page']//a[last()-1]/@href"
        self.link_xpath = "//td[@class='line4']/table//@href"
        self.box_xpath = "//div[@class='box_r_left']"

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'd.com.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
        }

        # params_xpath to crawl
        self.project_name_xpath = "//h2"
        self.loan_amount_xpath = "//li[@class='l_amount']/div"
        self.annual_return_xpath = "//li[@class='l_allot']/div"
        self.repayment_method_xpath = "//li[@class='l_paytype']/div"

    def parse(self, response):
        logging.info("=====GET SUCCESS=======")
        # last page
        last_page = response.xpath(self.last_page_xpath).extract()[0]
        # total page
        total_page = re.search("-0-(\d+).html", last_page).group(1)
        #
        for page in xrange(1, int(total_page)+1):
            yield scrapy.Request(url='http://d.com.cn/lend-0-0-0-{}.html'.format(page), headers=self.headers, dont_filter=True, callback=self.parse_page)

    def parse_page(self, response):
        logging.info('============REQUEST PAGE SUCCESSFULLY!!===============')
        box = response.xpath(self.box_xpath).extract()
        if box:
            box_no = len(box)
        else:
            box_no = 0
        for a_box in box:
            secondary_href = Selector(text=a_box).xpath("//div[@class='top_title_inner']/a/@href").extract()[0]
            yield scrapy.Request(url=secondary_href, dont_filter=True, callback=self.parse_item)

    def parse_item(self, response):
        logging.info('==========START CRAWLER=================')

        item = InvestmentItem()
        try:
            item['project_name'] = response.xpath(self.project_name_xpath).xpath("string(.)").extract()[0].strip().encode("utf-8")
        except:
            item['project_name'] = ''

        try:
            item['loan_amount'] = response.xpath(self.loan_amount_xpath).xpath("string(.)").extract()[0].strip().encode("utf-8")
        except:
            item['loan_amount'] = ''

        try:
            item['annual_return'] = response.xpath(self.annual_return_xpath).xpath("string(.)").extract()[0].strip().encode("utf-8")
        except:
            item['annual_return'] = ''

        try:
            item['repayment_method'] = response.xpath(self.repayment_method_xpath).xpath("string(.)").extract()[0].strip().encode("utf-8")
        except:
            item['repayment_method'] = ''

        item['secondary_href'] = response.url
        # print item
        yield item
