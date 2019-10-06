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



df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

# df.to_csv('E:/PythonData/Tushare/shares_list.csv')

df.to_csv('E:/PythonData/Tushare/shares_list.csv',encoding = "utf_8_sig")