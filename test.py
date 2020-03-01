from pyecharts import options as opts
from pyecharts.charts import Scatter
import pandas as pd


scatter1=Scatter()
# 价格均线
scatter1.set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                         yaxis_opts=opts.AxisOpts(is_scale=True),
                         datazoom_opts=[opts.DataZoomOpts()],
                         title_opts=opts.TitleOpts(title="test"))

df2 = pd.read_csv("F:\\Stock\\html_png_Total_day\\2019-10-10\\2019-10-10_Total_Day.csv")

print(df2['Final portfolio value'].shape[0])
x=range(df2['Final portfolio value'].shape[0])
y=df2['Final portfolio value']/10000

scatter1.add_xaxis(x)
scatter1.add_yaxis("sma",y)

scatter1.render(path='F:\\Stock/html_png_Total_day/aaa.html')