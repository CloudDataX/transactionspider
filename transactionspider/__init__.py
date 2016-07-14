import platform
import os
import codecs
import json
print "tansactionspider _init_"

StockCode = '0000001'
SysStr = 'Linux'
OrgId = ''
MinYear = ''
TransactionFolder = ''
TransactionSpiderLog = ''
Szse_StockPath = ''
TransactionFolder = ''
StockIndex = ''
StockNumsInJson = 0
SysStr = platform.system()

#Prepare folder and files
if(SysStr =="Windows"):
    TransactionFolder = r'D:\transactiondata\\'
elif(SysStr == "Linux"):
    TransactionFolder = r'/home/xproject/transactiondata'           
else:
    print "ERR/ OS unknown"
    os._exit()
TransactionSpiderLog = TransactionFolder + 'transactionSpider.log'
Szse_StockPath = TransactionFolder + 'szse_stock.json'


if (False == os.path.exists(TransactionFolder)):
    os.makedirs(TransactionFolder)
    
if (False == os.path.exists(Szse_StockPath)):
    print "szse_stock.json not exist!"

jsonSzse_stocks=json.loads(open(Szse_StockPath, 'rb').read())
if StockNumsInJson == 0:
    for jsonSzse_stock in jsonSzse_stocks['stockList']:
        StockNumsInJson=StockNumsInJson+1
    
    
    
if (False == os.path.exists(TransactionSpiderLog)):
    f= codecs.open(TransactionSpiderLog,'w','utf-8')
    writeData = '***'
    f.write(writeData)
    f.close()
    
    
    