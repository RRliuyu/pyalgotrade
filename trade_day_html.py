from pyalgotrade import strategy
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from pyalgotrade.stratanalyzer import trades
from pyalgotrade import plotter
import os
import datetime
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line,Kline,Scatter
import time



class MyStrategy(strategy.BacktestingStrategy):

    def __init__(self,feed,instrument,smaPeriod):
        super(MyStrategy, self).__init__(feed, 1000000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__pricesma=ma.SMA(feed[instrument].getPriceDataSeries(),smaPeriod)
        self.__rsi = rsi.RSI(feed[instrument].getPriceDataSeries(), smaPeriod)
        self.__volsma = ma.SMA(feed[instrument].getVolumeDataSeries(), smaPeriod)
        self.__vol=feed[instrument].getVolumeDataSeries()
        self.__chg = ma.SMA(feed[instrument].getExtraDataSeries(name="pct_chg"), 1)
        self.Buyday=[]
        self.Sellday=[]
        self.Buyprice=[]
        self.Sellprice=[]
        self.Barday = []
        self.Sma_price=[]
        self.Sma_vol = []
        self.money=[]
    def onEnterOk(self, position):
        execInfo=position.getEntryOrder().getExecutionInfo()
        self.info("Buy at $%.2f" %(execInfo.getPrice()))
        # MyStrategy.Buyday=self.__position.getEntryOrder().getExecutionInfo().getDateTime()+datetime.timedelta(days=1)
        self.Buyday.append(str(self.__position.getEntryOrder().getExecutionInfo().getDateTime()))
        self.Buyprice.append(execInfo.getPrice())

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("Sell at $%.2f" % (execInfo.getPrice()))
        self.Sellday.append(str(self.__position.getExitOrder().getExecutionInfo().getDateTime()))
        self.Sellprice.append(execInfo.getPrice())
        # time.sleep(0.05)
        # test = myStrategy.getBroker().getEquity()
        # print(test)
        # time.sleep(0.05)
        self.__position=None
    def getSMA(self):
        return self.__pricesma
    def getsmaVol(self):
        return  self.__volsma
    def getVol(self):
        return self.__vol
    def onBars(self, bars):
        self.money.append(myStrategy.getBroker().getEquity())


#######################################################################################################################
        # if self.__volsma[-1] is None:
        #     return
        # bar=bars[self.__instrument]
        # if self.__position is None:
        #     if bar.getVolume() > (self.__volsma[-1])*2:
        #         self.__position=self.enterLong(self.__instrument,1000,True)
        #             # elif bar.getVolume() < (self.__volsma[-1]) and not self.__position.exitActive():
        #             #     self.__position.exitMarket()
        # elif self.__chg[-1] > 9.8  and not self.__position.exitActive():
        #      self.__position.exitMarket()
        #      print(self.__chg[-1])
        # If a position was not opened, check if we should enter a long position.
        if self.__pricesma[-1] is None:
            return
        # print(round(self.__sma[-1],3))
        bar = bars[self.__instrument]
        self.Barday.append(str(bar.getDateTime()))
        self.Sma_price.append(self.__pricesma[-1])
        self.Sma_vol.append(self.__volsma[-1])

#######################################################################################################################
        if self.__position is None:
            if bar.getPrice() > self.__pricesma[-1]:
                shares = int(self.getBroker().getCash() * 0.5 / bars[self.__instrument].getPrice())
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
        # Check if we have to exit the position.
        elif bar.getPrice() < self.__pricesma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


def run_strategy(smaPeriod):
    df_new = pd.DataFrame(columns=('shares_ID', 'total number of trades','Profit times number of trades','Profit Percentage','Final portfolio value'))
    for (root,dirs,files) in os.walk("E:/Stock/Data_Day"):
        z=0
        for x in range(len(files)):
            z=z+1
            #K线图
            df = pd.read_csv("E:/Stock/Data_Day/"+files[x])
            df = df.sort_index(ascending=False).reset_index(drop=True)
            print("进度：", z / len(files) * 100, "%")
            date = df.xs('Date Time', axis=1).tolist()
            data = []
            vol = []
            for idx in df.index:
                row1 = [df.iloc[idx]['Open'], df.iloc[idx]['Close'], df.iloc[idx]['Low'], df.iloc[idx]['High']]
                row2 = df.iloc[idx]['Volume']
                data.append(row1)
                vol.append(row2)
            kline1 = Kline()
            line1 = Line()
            line2 = Line()
            line3 = Line()
            scatter1 = Scatter()
            scatter2 = Scatter()

            kline1.set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                                   yaxis_opts=opts.AxisOpts(is_scale=True),
                                   datazoom_opts=[opts.DataZoomOpts()])
            kline1.extend_axis(yaxis=opts.AxisOpts(type_='value', position='right'))
            kline1.extend_axis(yaxis=opts.AxisOpts(type_='value', position='right'))

            # 价格均线
            line1.set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                                   yaxis_opts=opts.AxisOpts(is_scale=True),
                                   datazoom_opts=[opts.DataZoomOpts()])
            # 成交量
            line2.set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                                  yaxis_opts=opts.AxisOpts(is_scale=True),
                                  datazoom_opts=[opts.DataZoomOpts()])
            #资金量
            line3.set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                                  yaxis_opts=opts.AxisOpts(is_scale=True),
                                  datazoom_opts=[opts.DataZoomOpts()])
            #买入点
            scatter1.set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                                     yaxis_opts=opts.AxisOpts(is_scale=True),
                                     datazoom_opts=[opts.DataZoomOpts()])
            #卖出点
            scatter2.set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                                     yaxis_opts=opts.AxisOpts(is_scale=True),
                                     datazoom_opts=[opts.DataZoomOpts()])

            kline1.add_xaxis(date)
            kline1.add_yaxis(files[x], data)
            line2.add_xaxis(date)
            line2.add_yaxis("vol",vol,yaxis_index=1,label_opts=opts.LabelOpts(is_show=False))


            feed = GenericBarFeed(Frequency.DAY,None,None)
            feed.addBarsFromCSV("fd", "E:/Stock/Data_Day/"+files[x])
            global  myStrategy
            myStrategy = MyStrategy(feed, "fd", smaPeriod)
            trade_situation = trades.Trades()
            myStrategy.attachAnalyzer(trade_situation)
            plt = plotter.StrategyPlotter(myStrategy)
            # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
            plt.getInstrumentSubplot("test").addDataSeries("SMA", myStrategy.getSMA())
            # Plot the simple returns on each bar.
            # plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())
            myStrategy.run()
            scatter1.add_xaxis(myStrategy.Buyday)
            scatter1.add_yaxis("Buy", myStrategy.Buyprice)
            scatter2.add_xaxis(myStrategy.Sellday)
            scatter2.add_yaxis("Sell", myStrategy.Sellprice)
            line1.add_xaxis(myStrategy.Barday)
            line1.add_yaxis("Price_SMA",myStrategy.Sma_price,label_opts=opts.LabelOpts(is_show=False))
            line3.add_xaxis(date)
            line3.add_yaxis("money", myStrategy.money,yaxis_index=2,label_opts=opts.LabelOpts(is_show=False))
            plt.savePlot("E:/Stock/html_png_Total_day/"+files[x]+".png")
            print(files[x]+" Final portfolio value:$%.2f" %myStrategy.getBroker().getEquity())
            print("total number of trades", trade_situation.getCount())
            print("Profit times number of trades ", trade_situation.getProfitableCount())
            if trade_situation.getCount() > 0:
                Percentage = trade_situation.getProfitableCount() / trade_situation.getCount()
                print("百分比",Percentage)
            else:
                Percentage = 0
                print("百分比", 0)
            df1= pd.DataFrame({"shares_ID": [files[x]],'total number of trades': [trade_situation.getCount()],'Profit times number of trades' :  trade_situation.getProfitableCount(),'Profit Percentage' : Percentage , 'Final portfolio value': [myStrategy.getBroker().getEquity()]})
            kline1.overlap(scatter1)
            kline1.overlap(scatter2)
            kline1.overlap(line1)
            kline1.overlap(line2)
            kline1.overlap(line3)
            kline1.render(path='E:\\Stock/html_png_Total_day/' + files[x] + '.html')
            df_new = pd.concat([df1,df_new], ignore_index=True)
    df_new.to_csv("E:/Stock/html_png_Total_day/Total_Min.csv", index=False)

# i=[240,244,248,252,256,260,264,268,272,276,280,284,288,292,294,298,302]
# for x in i :
run_strategy(18)