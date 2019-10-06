import pandas as pd
import numpy as np
from pyecharts import EffectScatter,Line,Overlap
from pyecharts.types import


df=pd.read_csv("E:/PythonData/CSV/000713.csv")
df['mean20']=df.Volume.rolling(window=20).mean()
outdf=df[(df['Volume']>df['mean20']*1.5)]

line1=Line()
line2=Line()
line3=Line()
es1=EffectScatter()
overlay=Overlap()

line1.add('Close',df.Date,df.Close,mark_point=['max','min'],is_datazoom_show=True)
es1.add=('test',outdf.Date,outdf.Close,xaxis_type='category')
line2.add("Volume",df.Date,df.Volume,mark_point=['max','min'],is_datazoom_show=True)
line3.add("Volume20",df.Date,df.mean20,mark_point=['max','min'],is_datazoom_show=True)

overlay.add(line1)
overlay.add(es1)
overlay.add(line2,yaxis_index=1,is_add_yaxis=True)
overlay.add(line3,yaxis_index=1,is_add_yaxis=True)
overlay.render("d:\\aaa.html")

