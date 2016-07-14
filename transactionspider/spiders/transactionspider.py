#! -*- coding:utf-8 -*-
# encoding: utf-8
from scrapy.spider import Spider  
from scrapy.selector import Selector
import scrapy
from scrapy.http import Request
import urllib2
import json
import datetime
import time
import urllib
import re
import socket
from scrapy import log
from transactionspider import SysStr,StockCode,Szse_StockPath


class TransactionSpider(scrapy.Spider):
    name = "transaction"
    #allowed_domains = ["cninfo.com.cn"]
    start_urls = ["http://www.cninfo.com.cn/cninfo-new/data/query"]
    transactionFolder = ''
    transactionSpiderLog = ''

    def parse(self, response):
        print 'TransactionSpider.parse reponse.url', response.url
        queryUrl ='http://www.cninfo.com.cn/cninfo-new/data/query'
        
        jsonSzse_stocks=json.loads(open(Szse_StockPath, 'rb').read())
        if self.stockNumsInAllStockJson == 0:
            for jsonSzse_stock in jsonSzse_stocks['stockList']:
                self.stockNumsInAllStockJson=self.stockNumsInAllStockJson+1
            jsonStockIndex=80
            
        if(0<=jsonStockIndex and jsonStockIndex<self.stockNumsInAllStockJson):      
              
            code=jsonSzse_stocks['stockList'][jsonStockIndex]['code']
            orgId=jsonSzse_stocks['stockList'][jsonStockIndex]['orgId']
            stock=jsonSzse_stocks['stockList'][jsonStockIndex]['code']+'%2C'+jsonSzse_stocks['stockList'][jsonStockIndex]['orgId']
            pageNum=1
            yield Request(self.generateUrl(queryUrl,stock,pageNum,jsonStockIndex), callback=self.parseDetail,meta={'code':code,'orgId':orgId,'pageNum':pageNum,'jsonStockIndex':jsonStockIndex})
        
        print "!!", SysStr
            
    def parseDetail(self,response):
        return
            

        