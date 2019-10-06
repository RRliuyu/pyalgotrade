import pandas as pd
import tushare as ts
import time
#获取数据
pro = ts.pro_api('5f37df276dab4fff9a3783499fd18174ec34caf4a84dc1e953c7d987')



df1 = pd.read_csv('E:/Stock/shares_list.csv')
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)


for i in range(df1.ts_code.shape[0]):
    #下载数据
    df2 = ts.pro_bar(ts_code=df1.iloc[i,1], adj='qfq', start_date='20150101', end_date='20190818', freq='60min',retry_count=10)
    #将成交量由1手改为100股
    df2.vol = df2.vol * 100
    #将成交额由千元改为元
    df2.amount = df2.amount * 1000
    # 数据存盘
    df2.to_csv("E:/Stock/Tushare_min/"+df1.iloc[i,1]+".csv")
    # 读出数据，DataFrame格式
    df2 = pd.read_csv("E:/Stock/Tushare_min/"+df1.iloc[i,1]+".csv")
    # 从df中选取数据段，改变段名；新段'Adj Close'使用原有段'close'的数据
    df3 = pd.DataFrame({'Date Time' : df2['trade_time'], 'Open' : df2['open'],
                    'High' : df2['high'],'Close' : df2['close'],
                    'Low' : df2['low'],'Volume' : df2['vol'],
                    'amount' : df2['amount']})
    # 删除包含09:30:00的行
    df3 = df3[~df3['Date Time'].str.contains("09:30:00")]
    #调整时间格式(GenericBarFeed)[60min数据不用调整]
    # df3['Date Time']=df3['Date Time'].apply(str)
    # df3['Date Time']=df3['Date Time'].map(lambda x :'%s-%s-%s'%(x[0:4],x[4:6],x[6:8])+' 00:00:00')
    # #调整时间格式(yahoofeed.Feed)
    # df3['Date Time']=df3['Date Time'].apply(str)
    # df3['Date Time']=df3['Date Time'].map(lambda x :'%s-%s-%s'%(x[0:4],x[4:6],x[6:8]))
    df3.to_csv("E:/Stock/Data_Min_original/"+df1.iloc[i,1]+".csv", index=False)
    print("完成进度:",i/df1.ts_code.shape[0]*100,"%")