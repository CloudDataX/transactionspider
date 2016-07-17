#! -*- coding:utf-8 -*-
# encoding: utf-8
from scrapy.spider import Spider  
from scrapy.http import Request
import transactionspider
#from transactionspider import myvariables
#from transactionspider import StockNumsInAllStockJson,JsonSzse_Stocks,StockStartIndex,StockEndIndex


class TransactionSpider(Spider):
    name = "transaction"
    #allowed_domains = ["cninfo.com.cn"]
    start_urls = ["http://www.cninfo.com.cn/cninfo-new/index"]
    queryUrl ='http://www.cninfo.com.cn/cninfo-new/data/query'
    downloadUrl = 'http://www.cninfo.com.cn/cninfo-new/data/download'
    jsonStockIndex = 0
    
    def parse(self, response):
        print 'TransactionSpider.parse reponse.url', response.url
        self.jsonStockIndex += 1
            
        if(transactionspider.StockStartIndex<=self.jsonStockIndex and self.jsonStockIndex<min(transactionspider.StockNumsInAllStockJson, transactionspider.StockEndIndex)):                    
            code=transactionspider.JsonSzse_Stocks['stockList'][self.jsonStockIndex]['code']
            orgId=transactionspider.JsonSzse_Stocks['stockList'][self.jsonStockIndex]['orgId']
            
            yield Request(self.queryUrl, callback=self.parse,meta={'code':code,'orgId':orgId,'jsonStockIndex':self.jsonStockIndex}) 
        elif (self.jsonStockIndex==self.stockNumsInAllStockJson):
            print '====================================='
            print 'fetch stock data finished,please check if have fail lists in result/szse_stock_failList.json'
            print '====================================='
        else:
            print '====================================='
            print 'fetch stock data fail,exit!!! jsonStockIndex=',self.jsonStockIndex,response.url,response.body
            print 'please check fail lists in result/szse_stock_failList.json'
            print '====================================='
            
            

        