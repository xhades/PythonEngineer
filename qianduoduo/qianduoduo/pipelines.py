# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from .items import *


class QianduoduoPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        # self.file = open('document','wb')

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            port=settings['MYSQL_PORT'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb',**dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        return item

    def _do_upinsert(self, conn, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                print 'NOT ANY DATA IN ITEM'
        if valid:
            mysql = "INSERT IGNORE INTO `qianduoduo`(`project_name`,`loan_amount`,`annual_return`, `repayment_method`, `secondary_url`) values(%s,%s,%s,%s,%s)"
            result = conn.execute(mysql,
                                  (item['project_name'],
                                   item['loan_amount'],
                                   item['annual_return'],
                                   item['repayment_method'],
                                   item['secondary_href']
                                   ))
            if result:
                print 'added a record'
            else:
                print 'failed insert into table `qianduoduo`'

# CREATE TABLE  qianduoduo (
# id  INT NOT NULL AUTO_INCREMENT,
# project_name varchar(255) default NULL comment "项目名称",
# loan_amount varchar(120) default null comment "借款额度",
# annual_return varchar(55) default null comment "历史平均年化率",
# repayment_method varchar(55) default null comment "还款方式",
# secondary_url varchar(255) default null comment"二级页面链接",
# primary key (id),
# unique key (secondary_url)
# ) ENGINE=INNODB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;