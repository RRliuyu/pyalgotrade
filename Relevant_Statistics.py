import pandas as pd
import os


# for (root, dirs, files) in os.walk("E:/Stock/Data_Day"):
#     z = 0
#     for x in range(len(files)):
#         z = z + 1
#         print("进度：", z / len(files) * 100, "%")
#
#         df=pd.read_csv('E:/Stock/Data_Day/' + files[x])


df=pd.read_csv('E:/Stock/Data_Day/000001.SZ.csv')
print(df[df['pct_change']]>0)