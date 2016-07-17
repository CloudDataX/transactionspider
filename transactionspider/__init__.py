import platform
import os
import codecs
import json
import time

print "tansactionspider _init_"
StockCode = ''
TransactionFolder = ''
TransactionSpiderLog = ''
Szse_StockPath = ''
SysStr = platform.system()
StockNumsInAllStockJson = 0
JsonSzse_Stocks = ''
ProcessIndex = 1
StockStartIndex = 0
StockEndIndex = 9999
MaxYear = time.strftime('%Y',time.localtime(time.time()))
print "!!MaxYear:", MaxYear

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
    
if (False == os.path.exists(TransactionSpiderLog)):
    f= codecs.open(TransactionSpiderLog,'w','utf-8')
    writeData = '***'
    f.write(writeData)
    f.close()

#Get All stock Num
JsonSzse_Stocks=json.loads(open(Szse_StockPath, 'rb').read())
for jsonSzse_stock in JsonSzse_Stocks['stockList']:
    StockNumsInAllStockJson=StockNumsInAllStockJson+1
print "Total stock Num is:", StockNumsInAllStockJson    


    
# Use 1.txt 2.txt 3.txt ... to distribute different process
while (ProcessIndex < 5):
    ProcessFile = TransactionFolder + str(ProcessIndex) + '.txt'
    if ( False == os.path.exists(ProcessFile)):
        f= codecs.open(ProcessFile,'w','utf-8')
        writeData = '{}'
        f.write(writeData)
        f.close()
        break
    else:
        ProcessIndex += 1
        
if ProcessIndex == 1:
    StockStartIndex = 0
    StockEndIndex = 800
elif ProcessIndex == 2:
    StockStartIndex = 800
    StockEndIndex = 1600
elif ProcessIndex == 3:
    StockStartIndex = 1600
    StockEndIndex = 2400
elif ProcessIndex == 4:
    StockStartIndex = 2400
    StockEndIndex = 3200
