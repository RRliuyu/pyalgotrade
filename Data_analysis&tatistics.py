import pandas as pd
import time
import os

#记录开始时间
start =time.perf_counter()

now=int(time.time())

#今日时间
timeStruct=time.localtime(now)
strTime1=time.strftime("%Y-%m-%d",timeStruct)
strTime2=time.strftime("%Y-%m-%d",timeStruct)+" 00:00:00"

#判断今日是否是周一
if timeStruct.tm_wday==0:
    day1=3;day2=4;day3=5;day4=6;day5=7
#判断今日是否是周二
if timeStruct.tm_wday==1:
    day1=1;day2=4;day3=5;day4=6;day5=7
#判断今日是否是周三
if timeStruct.tm_wday==2:
    day1=1;day2=2;day3=5;day4=6;day5=7
#判断今日是否是周四
if timeStruct.tm_wday==3:
    day1=1;day2=2;day3=3;day4=6;day5=7
#判断今日是否是周五
if timeStruct.tm_wday==4:
    day1=1;day2=2;day3=3;day4=4;day5=7

#前1日时间
timeStruct1=time.localtime(now-day1*86400)
one_day_ago1=time.strftime("%Y-%m-%d",timeStruct1)
one_day_ago2=time.strftime("%Y-%m-%d",timeStruct1)+" 00:00:00"

#前2日时间
timeStruct2=time.localtime(now-day2*86400)
two_day_ago1=time.strftime("%Y-%m-%d",timeStruct2)
two_day_ago2=time.strftime("%Y-%m-%d",timeStruct2)+" 00:00:00"

#前3日时间
timeStruct3=time.localtime(now-day3*86400)
three_day_ago1=time.strftime("%Y-%m-%d",timeStruct3)
three_day_ago2=time.strftime("%Y-%m-%d",timeStruct3)+" 00:00:00"

#前4日时间
timeStruct4=time.localtime(now-day4*86400)
four_day_ago1=time.strftime("%Y-%m-%d",timeStruct4)
four_day_ago2=time.strftime("%Y-%m-%d",timeStruct4)+" 00:00:00"

#前5日时间
timeStruct5=time.localtime(now-day5*86400)
five_day_ago1=time.strftime("%Y-%m-%d",timeStruct5)
five_day_ago2=time.strftime("%Y-%m-%d",timeStruct5)+" 00:00:00"

date_list = [strTime2]
date_list1 = [one_day_ago2,strTime2]
date_list2 = [two_day_ago2, one_day_ago2,strTime2]
date_list3 = [three_day_ago2, two_day_ago2, one_day_ago2,strTime2]
date_list4 = [four_day_ago2,three_day_ago2, two_day_ago2, one_day_ago2,strTime2]
date_list5 = [five_day_ago2,four_day_ago2,three_day_ago2, two_day_ago2, one_day_ago2,strTime2]

# #清空目录
# os.remove('E:/Stock/Data_analysis&statistics/' + strTime1)
#创建保持目录
os.mkdir('E:/Stock/Data_analysis&statistics/' + strTime1)

#----------------------------------------获取股票列表(以当日所有股票查看）--------------------------------------------

# df1 = pd.read_csv('E:/Stock/shares_list.csv')
#
# for i in range(df1.ts_code.shape[0]):
#     df2 = pd.read_csv('E:/Stock/Data_Day_original/' + strTime1 + "/" + df1.iloc[i, 1]+'.csv')
#     if df2[(df2['Date Time'].isin(date_list)) & (df2['pct_chg'] > 0)].shape[0] > 4 :
#         file_name = 'E:/Stock/Data_analysis&statistics/news.csv'
#         with open(file_name, 'a+') as file_object:
#             file_object.write(df1.iloc[i, 1]+'\n')

#-----------------------------------------获取股票列表（以当日破18日均线的股票查看）-------------------------------------

# df1 = pd.read_csv('E:/Stock/html_png_Total_day/'+strTime1+'/'+strTime1+'_Today_tradable_stocks.csv')

# for i in range(df1.shares_ID.shape[0]):
#     df2 = pd.read_csv('E:/Stock/Data_Day_original/' + strTime1 + "/" + df1.iloc[i, 1])
#     if df2[(df2['Date Time'].isin(date_list)) & (df2['pct_chg'] > 0)].shape[0] > 4 :
#         file_name = 'E:/Stock/Data_analysis&statistics/news.csv'
#         with open(file_name, 'a+') as file_object:
#             file_object.write(df1.iloc[i, 1]+'\n')

#-----------------------------------------获取股票列表（以前1日破18日均线的股票查看）-------------------------------------

df1 = pd.read_csv('E:/Stock/html_png_Total_day/'+one_day_ago1+'/'+one_day_ago1+'_Today_tradable_stocks.csv')

count1=df1.shape[0]
count2=0

for i in range(df1.shares_ID.shape[0]):
    df2 = pd.read_csv('E:/Stock/Data_Day_original/' + strTime1 + "/" + df1.iloc[i, 1]+".csv")
    if df2[(df2['Date Time'].isin(date_list)) & (df2['pct_chg'] > 0)].shape[0] >= 1 :
        count2=count2+1
        file_name = 'E:/Stock/Data_analysis&statistics/'+strTime1+'/one_day_ago1.csv'
        with open(file_name, 'a+') as file_object:
            file_object.write(df1.iloc[i, 1] + '\t')
            file_object.write(str(df1.iloc[i, 6]) + '\n')

if count1==0:
    count=str(0)
else:
    count=str(count2/count1)

file_name = 'E:/Stock/Data_analysis&statistics/'+strTime1+'/one_day_ago1.csv'
with open(file_name, 'a+') as file_object:
    file_object.write("前1日破18日均线的股票数后本日继续上涨股票/前1日破18日均线的股票数"+'\n')
    file_object.write(count)

#-----------------------------------------获取股票列表（以前2日破18日均线的股票查看）-------------------------------------

df1 = pd.read_csv('E:/Stock/html_png_Total_day/'+two_day_ago1+'/'+two_day_ago1+'_Today_tradable_stocks.csv')

count1=df1.shape[0]
count2=0

for i in range(df1.shares_ID.shape[0]):
    df2 = pd.read_csv('E:/Stock/Data_Day_original/' + strTime1 + "/" + df1.iloc[i, 1]+".csv")
    if df2[(df2['Date Time'].isin(date_list1)) & (df2['pct_chg'] > 0)].shape[0] >= 2 :
        count2=count2+1
        file_name = 'E:/Stock/Data_analysis&statistics/'+strTime1+'/two_day_ago1.csv'
        with open(file_name, 'a+') as file_object:
            file_object.write(df1.iloc[i,1] + '\t')
            file_object.write(str(df1.iloc[i,6]) + '\n')

if count1==0:
    count=str(0)
else:
    count=str(count2/count1)

file_name = 'E:/Stock/Data_analysis&statistics/'+strTime1+'/two_day_ago1.csv'
with open(file_name, 'a+') as file_object:
    file_object.write("前2日破18日均线的股票数后继续两天上涨股票/前2日破18日均线的股票数"+'\n')
    file_object.write(count)

#-----------------------------------------获取股票列表（以前3日破18日均线的股票查看）-------------------------------------

df1 = pd.read_csv('E:/Stock/html_png_Total_day/'+three_day_ago1+'/'+three_day_ago1+'_Today_tradable_stocks.csv')

count1=df1.shape[0]
count2=0

for i in range(df1.shares_ID.shape[0]):
    df2 = pd.read_csv('E:/Stock/Data_Day_original/' + strTime1 + "/" + df1.iloc[i, 1]+".csv")
    if df2[(df2['Date Time'].isin(date_list2)) & (df2['pct_chg'] > 0)].shape[0] >= 3 :
        count2=count2+1
        file_name = 'E:/Stock/Data_analysis&statistics/'+strTime1+'/three_day_ago1.csv'
        with open(file_name, 'a+') as file_object:
            file_object.write(df1.iloc[i, 1] + '\t')
            file_object.write(str(df1.iloc[i, 6]) + '\n')

if count1==0:
    count=str(0)
else:
    count=str(count2/count1)

file_name = 'E:/Stock/Data_analysis&statistics/'+strTime1+'/three_day_ago1.csv'
with open(file_name, 'a+') as file_object:
    file_object.write("前3日破18日均线的股票数后继续三天上涨股票/前3日破18日均线的股票数"+'\n')
    file_object.write(count)

# -----------------------------------------获取股票列表（以指定日破18日均线的股票查看）-------------------------------------








#记录结束时间
end = time.perf_counter()
#打印运行时间
print('Running time: %s Seconds'%(end-start))