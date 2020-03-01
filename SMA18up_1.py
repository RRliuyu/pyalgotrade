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
print(one_day_ago1)

#前2日时间
timeStruct2=time.localtime(now-day2*86400)
two_day_ago1=time.strftime("%Y-%m-%d",timeStruct2)
two_day_ago2=time.strftime("%Y-%m-%d",timeStruct2)+" 00:00:00"
print(two_day_ago1)

#前3日时间
timeStruct3=time.localtime(now-day3*86400)
three_day_ago1=time.strftime("%Y-%m-%d",timeStruct3)
three_day_ago2=time.strftime("%Y-%m-%d",timeStruct3)+" 00:00:00"
print(three_day_ago1)

#前4日时间
timeStruct4=time.localtime(now-day4*86400)
four_day_ago1=time.strftime("%Y-%m-%d",timeStruct4)
four_day_ago2=time.strftime("%Y-%m-%d",timeStruct4)+" 00:00:00"
print(four_day_ago1)

#前5日时间
timeStruct5=time.localtime(now-day5*86400)
five_day_ago1=time.strftime("%Y-%m-%d",timeStruct5)
five_day_ago2=time.strftime("%Y-%m-%d",timeStruct5)+" 00:00:00"
print(five_day_ago1)

date_list = [strTime2]
date_list1 = [one_day_ago2,strTime2]
date_list2 = [two_day_ago2, one_day_ago2,strTime2]
date_list3 = [three_day_ago2, two_day_ago2, one_day_ago2,strTime2]
date_list4 = [four_day_ago2,three_day_ago2, two_day_ago2, one_day_ago2,strTime2]
date_list5 = [five_day_ago2,four_day_ago2,three_day_ago2, two_day_ago2, one_day_ago2,strTime2]

#-----------------------------------------获取股票列表（以前1日破18日均线的股票查看）-------------------------------------

# df1 = pd.read_csv('F:/Stock/html_png_Total_day/'+three_day_ago1+'/'+three_day_ago1+'_Today_tradable_stocks.csv')
#
# count1=df1.shape[0]
# count2=0
#
# for i in range(df1.shares_ID.shape[0]):
#     df2 = pd.read_csv('F:/Stock/Data_Day_original/' + strTime1 + "/" + df1.iloc[i, 1]+".csv")
#     if  df2.pct_chg.head(1).sum() > 7 :
#         count2=count2+1
#         file_name = 'F:/Stock/Data_analysis&statistics/'+strTime1+'/one_day_ago1_sma18up.csv'
#         with open(file_name, 'a+') as file_object:
#             file_object.write(df1.iloc[i, 1] + '\t')
#             file_object.write(str(df1.iloc[i, 6]) + '\n')


#-----------------------------------------获取股票列表（以前2日破18日均线的股票查看）-------------------------------------

df1 = pd.read_csv('F:/Stock/html_png_Total_day/'+two_day_ago1+'/'+two_day_ago1+'_Today_tradable_stocks.csv')

count1=df1.shape[0]
count2=0

for i in range(df1.shares_ID.shape[0]):
    df2 = pd.read_csv('F:/Stock/Data_Day_original/' + strTime1 + "/" + df1.iloc[i, 1]+".csv")
    if  df2.pct_chg.head(2).sum() > 5 :
        count2=count2+1
        file_name = 'F:/Stock/Data_analysis&statistics/'+strTime1+'/two_day_ago1_sma18up.csv'
        with open(file_name, 'a+') as file_object:
            file_object.write(df1.iloc[i, 1] + '\t')
            file_object.write(str(df1.iloc[i, 6]) + '\n')

#-----------------------------------------获取股票列表（以前3日破18日均线的股票查看）-------------------------------------

df1 = pd.read_csv('F:/Stock/html_png_Total_day/'+three_day_ago1+'/'+three_day_ago1+'_Today_tradable_stocks.csv')

count1=df1.shape[0]
count2=0

for i in range(df1.shares_ID.shape[0]):
    df2 = pd.read_csv('F:/Stock/Data_Day_original/' + strTime1 + "/" + df1.iloc[i, 1]+".csv")
    if  df2.pct_chg.head(3).sum() > 5 :
        count2=count2+1
        file_name = 'F:/Stock/Data_analysis&statistics/'+strTime1+'/three_day_ago1_sma18up.csv'
        with open(file_name, 'a+') as file_object:
            file_object.write(df1.iloc[i, 1] + '\t')
            file_object.write(str(df1.iloc[i, 6]) + '\n')

#-----------------------------------------获取股票列表（以前4日破18日均线的股票查看）-------------------------------------

df1 = pd.read_csv('F:/Stock/html_png_Total_day/'+four_day_ago1+'/'+four_day_ago1+'_Today_tradable_stocks.csv')

count1=df1.shape[0]
count2=0

for i in range(df1.shares_ID.shape[0]):
    df2 = pd.read_csv('F:/Stock/Data_Day_original/' + strTime1 + "/" + df1.iloc[i, 1]+".csv")
    if  df2.pct_chg.head(4).sum() > 5 :
        count2=count2+1
        file_name = 'F:/Stock/Data_analysis&statistics/'+strTime1+'/four_day_ago1_sma18up.csv'
        with open(file_name, 'a+') as file_object:
            file_object.write(df1.iloc[i, 1] + '\t')
            file_object.write(str(df1.iloc[i, 6]) + '\n')


#-----------------------------------------获取股票列表（以前5日破18日均线的股票查看）-------------------------------------

df1 = pd.read_csv('F:/Stock/html_png_Total_day/'+five_day_ago1+'/'+five_day_ago1+'_Today_tradable_stocks.csv')

count1=df1.shape[0]
count2=0

for i in range(df1.shares_ID.shape[0]):
    df2 = pd.read_csv('F:/Stock/Data_Day_original/' + strTime1 + "/" + df1.iloc[i, 1]+".csv")
    if  df2.pct_chg.head(5).sum() > 5 :
        count2=count2+1
        file_name = 'F:/Stock/Data_analysis&statistics/'+strTime1+'/five_day_ago1_sma18up.csv'
        with open(file_name, 'a+') as file_object:
            file_object.write(df1.iloc[i, 1] + '\t')
            file_object.write(str(df1.iloc[i, 6]) + '\n')
