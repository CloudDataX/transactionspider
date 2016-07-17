#! -*- coding:utf-8 -*-
# encoding: utf-8
from scrapy.http import HtmlResponse
import time
import urllib
import urllib2
import httplib
import cookielib
from urllib import urlencode
from urllib import unquote
import json

from transactionspider import StockCode,MaxYear

class TransactionMiddleware(object):
    start_urls = ["http://www.cninfo.com.cn/cninfo-new/index"]
    queryUrl ='http://www.cninfo.com.cn/cninfo-new/data/query'
    downloadUrl = 'http://www.cninfo.com.cn/cninfo-new/data/download'
    
    def __init__(self, options, max_sum):
        self.options = options
        self.max_sum = max_sum
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            options=crawler.settings.get('PHANTOMJS_OPTIONS', {}),
            max_sum=crawler.settings.get('PHANTOMJS_MAXSUM', 2)
        )
        
    def process_request(self, request, spider):
        stockCode = StockCode
        service_args = ['--load-image=false', '--disk-cache=true']
        url = request.url
        postdata = ''
        head = ''
        startYear = 0
        print "Start process_request: request:", request
        #request.url = startUrl return response with queryUrl to parse 
        if (self.start_urls == request.url[0:len(self.startUrl)]):
            print "Start URL"
            if(None==request.meta.get('jsonStockIndex', None)):
                jsonStockIndex=0
            else:
                jsonStockIndex =request.meta['jsonStockIndex']
            content='jsonStockIndex='+str(jsonStockIndex)
            return HtmlResponse(self.queryUrl, encoding='utf-8', status=200, body=content)
        
        if (request.queryUrl[0:len(self.queryUrl)] == self.queryUrl):
            heads = { 'Accept':'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    'Connection':'keep-alive',
                    'Content-Length':'32',
                    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                    'Cookie':'JSESSIONID=DA9BC88402AD775B071E9DAF29CAB669',
                    'Host':'www.cninfo.com.cn',
                    'Origin':'http://www.cninfo.com.cn',
                    'Referer':'http://www.cninfo.com.cn/cninfo-new/index',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
                    'X-Requested-With':'XMLHttpRequest' } 
            postdata = 'keyWord=' + stockCode + '&maxNum=10&hq_or_cw=1'
            #postdata="K_code=&&market=sh&&type=hq&&code=600000&&orgid=gssh0600000&&minYear=1999&&maxYear=2016&&hq_code=600000&&hq_k_code=&&cw_code=&&cw_k_code="
            
            newRequest = urllib2.Request(self.queryUrl,postdata,heads)
            response = urllib2.urlopen(newRequest,None, 10)
            content = response.read()
            #set_cookie = response.info()['Set-Cookie']
            response = HtmlResponse(self.queryUrl, encoding='utf-8', status=200, body=content)    
            #get Json data and startYear
            jsonResponse = json.loads(response.body)
            startYear = jsonResponse['startTime']
            market = jsonResponse['market']
            orgid = jsonResponse['orgid']
            code = jsonResponse['code']
            
            print "Middlewares queryUrl, stockCode: ",stockCode, ' startTime:',startYear
        
        if startYear != 0:
            boundary = '----WebKitFormBoundaryA5otDEFHCmAaF76I'
            heads = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'Content-Length':'1107',
                    'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundaryA5otDEFHCmAaF76I',
                    'Cookie':'JSESSIONID=851F059690F838B7498EEDC42F6B5BD9',
                    'Host':'www.cninfo.com.cn',
                    'Origin':'http://www.cninfo.com.cn',
                    'Referer':'http://www.cninfo.com.cn/cninfo-new/index',
                    'Upgrade-Insecure-Requests':'1',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36' } 
            #postdata = 'keyWord=' + globalvariables.StockCode + '&maxNum=10&hq_or_cw=1'
            postdata='K_code=&&market='+market+'&&type=hq&&code='+code+'&&orgid='+orgid+'&&minYear='+startYear+'&&maxYear='+MaxYear+'&&hq_code='+code+'&&hq_k_code=&&cw_code=&&cw_k_code='
        
            newRequest = urllib2.Request(self.downloadUrl,postdata,heads)
            response = urllib2.urlopen(newRequest,None, 10)
            content = response.read()
            #set_cookie = response.info()['Set-Cookie']
            response = HtmlResponse(self.queryUrl, encoding='utf-8', status=200, body=content)   
        
        return response
    
    
