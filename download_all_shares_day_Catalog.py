import pandas as pd
import tushare as ts
import time
import os

now=int(time.time())
timeStruct=time.localtime(now)
strTime1=time.strftime("%Y-%m-%d",timeStruct)
strTime2=time.strftime("%Y-%m-%d",timeStruct)+" 00:00:00"

os.mkdir("E:/Stock/Data_Day_original/Catalog/")
os.mkdir("E:/Stock/Tushare_day/Catalog/" )

#设置下载秘钥
pro = ts.pro_api('5f37df276dab4fff9a3783499fd18174ec34caf4a84dc1e953c7d987')
#获取股票列表
df1 = pd.read_csv('E:/Stock/shares_list.csv')
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)


for i in range(df1.ts_code.shape[0]):
    #下载数据

    df2 = ts.pro_bar(ts_code=df1.iloc[i, 1], adj='qfq', retry_count=20,start_date='20071101', end_date='20191231')

    #将成交量由1手改为100股
    df2.vol = df2.vol * 100
    #将成交额由千元改为元
    df2.amount = df2.amount * 1000


    # 数据存盘
    print(df1.iloc[i,1])
    df2.to_csv('E:/Stock/Tushare_day/Catalog/'+df1.iloc[i,1]+".csv")
    # 读出数据，DataFrame格式
    df2 = pd.read_csv('E:/Stock/Tushare_day/Catalog/'+df1.iloc[i,1]+".csv")
    # 从df中选取数据段，改变段名；新段'Adj Close'使用原有段'close'的数据
    df3 = pd.DataFrame({'Date Time' : df2['trade_date'], 'Open' : df2['open'],
                        'High' : df2['high'],'Close' : df2['close'],
                        'Low' : df2['low'],'Volume' : df2['vol'],
                        'Adj Close':df2['close'],
                        'pre_close' : df2['pre_close'],
                        'change' : df2['change'],
                        'pct_chg' : df2['pct_chg'],
                        'amount' : df2['amount']})
    #调整时间格式(GenericBarFeed)
    df3['Date Time']=df3['Date Time'].apply(str)
    df3['Date Time']=df3['Date Time'].map(lambda x :'%s-%s-%s'%(x[0:4],x[4:6],x[6:8])+' 00:00:00')
    # #调整时间格式(yahoofeed.Feed)
    # df3['Date Time']=df3['Date Time'].apply(str)
    # df3['Date Time']=df3['Date Time'].map(lambda x :'%s-%s-%s'%(x[0:4],x[4:6],x[6:8]))
    df3.to_csv("E:/Stock/Data_Day_original/Catalog/"+df1.iloc[i,1] +".csv", index=False)
    print("完成进度:", i / df1.ts_code.shape[0] * 100, "%")