import tushare as ts
import pandas as pd
import datetime
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#获取数据
pro = ts.pro_api('5f37df276dab4fff9a3783499fd18174ec34caf4a84dc1e953c7d987')
df = ts.pro_bar(ts_code='600115.SH',adj='qfq', start_date='20140101', end_date='20190818',freq='60min')
# 数据存盘
df.to_csv('E:/PythonData/Tushare_min/600115.csv')
# 读出数据，DataFrame格式
df = pd.read_csv('E:/PythonData/Tushare_min/600115.csv')
# 从df中选取数据段，改变段名；新段'Adj Close'使用原有段'close'的数据
df2 = pd.DataFrame({'Date Time' : df['trade_time'], 'Open' : df['open'],
                    'High' : df['high'],'Close' : df['close'],
                    'Low' : df['low'],'Volume' : df['vol'],
                    'amount' : df['amount']})
#删除包含09:30:00的行
df2=df2[~df2['Date Time'].str.contains("09:30:00")]

#调整时间格式(GenericBarFeed)
# df2['Date Time']=df2['Date Time'].apply(str)
# df2['Date Time']=df2['Date Time'].map(lambda x :'%s-%s-%s'%(x[0:4],x[4:6],x[6:8])+' 00:00:00')

# #调整时间格式(yahoofeed.Feed)
# df2['Date Time']=df2['Date Time'].apply(str)
# df2['Date Time']=df2['Date Time'].map(lambda x :'%s-%s-%s'%(x[0:4],x[4:6],x[6:8]))

df2.to_csv("E:/PythonData/CSV_min/600115.csv", index=False)