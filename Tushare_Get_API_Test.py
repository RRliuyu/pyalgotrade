import tushare as ts
import pandas as pd
import datetime
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#获取数据
pro = ts.pro_api('5f37df276dab4fff9a3783499fd18174ec34caf4a84dc1e953c7d987')
ts.set_token('5f37df276dab4fff9a3783499fd18174ec34caf4a84dc1e953c7d987')

# df1 = pro.daily(ts_code='600018.SH', start_date='20170815', end_date='20190830')
# df1.vol=df1.vol*100
# df1.amount=df1.amount*1000

# df2 = ts.pro_bar(ts_code='600111.SH',adj='qfq', start_date='20190101', end_date='20190825')
# #
# df3 = pro.fut_basic(exchange='CFFEX', fut_type='1')
#
# # df4 = pro.index_basic(market='CSI')
#
# df5 = pro.fut_daily(ts_code='IF1908.CFX')

# df5=pro.cb_issue(ts_code='110030.SH')

#可转债
df = pro.cb_basic(fields='ts_code,reset_clause,conv_clause')

# df1 = pro.cb_issue(ts_code='125002.SZ')

# df = pro.cb_daily(trade_date='20190719')


print("-----------------------------")
print(df)
print("*****************************")
# print(df1)
print("-----------------------------")

df.to_csv("E:/aaa.csv")

print("ookk")
