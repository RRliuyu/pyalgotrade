import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line,Kline,Scatter

kline1 = Kline()
kline2 = Kline()





kline1.set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                       yaxis_opts=opts.AxisOpts(is_scale=True),
                       datazoom_opts=[opts.DataZoomOpts()])
kline1.extend_axis(yaxis=opts.AxisOpts(type_='value', position='right'))
kline1.extend_axis(yaxis=opts.AxisOpts(type_='value', position='right'))


kline2.set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                       yaxis_opts=opts.AxisOpts(is_scale=True),
                       datazoom_opts=[opts.DataZoomOpts()])
kline2.extend_axis(yaxis=opts.AxisOpts(type_='value', position='right'))
kline2.extend_axis(yaxis=opts.AxisOpts(type_='value', position='right'))



df = pd.read_csv('F:/Stock/kline.csv')

str1=str(df.iloc[0,1])
str2=str(df.iloc[1,1])

#-------------------------------------------------------------------------------------------------------------------

df1 = pd.read_csv('F:/Stock/Data_Day/' + df.iloc[0, 1] + ".csv")
df1 = df1.sort_index(ascending=False).reset_index(drop=True)
date1 = df1.xs('Date Time', axis=1).tolist()
data1 = []
vol1 = []
for idx1 in df1.index:
    row1 = [df1.iloc[idx1]['Open'], df1.iloc[idx1]['Close'], df1.iloc[idx1]['Low'], df1.iloc[idx1]['High']]
    row2 = df1.iloc[idx1]['Volume']
    data1.append(row1)
    vol1.append(row2)
kline1.add_xaxis(date1)
kline1.add_yaxis(str1, data1)

#-------------------------------------------------------------------------------------------------------------------

df2 = pd.read_csv('F:/Stock/Data_Day/' + df.iloc[1, 1] + ".csv")
df2 = df2.sort_index(ascending=False).reset_index(drop=True)
date2 = df2.xs('Date Time', axis=1).tolist()
data2 = []
vol2 = []
for idx2 in df2.index:
    row3 = [df2.iloc[idx2]['Open'], df2.iloc[idx2]['Close'], df2.iloc[idx2]['Low'], df2.iloc[idx2]['High']]
    row4 = df2.iloc[idx2]['Volume']
    data2.append(row3)
    vol2.append(row4)
print(date2)
kline2.add_xaxis(date2)
kline2.add_yaxis(str2, data2)
kline1.overlap(kline2)


kline1.render(path='F:\\Stock/Kline.html')


