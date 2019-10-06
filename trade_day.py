from pyalgotrade import strategy
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from pyalgotrade.stratanalyzer import trades
from pyalgotrade.stratanalyzer import returns
from pyalgotrade import plotter
import os
import pandas as pd
import time
#记录开始时间
start =time.perf_counter()

now=int(time.time())
timeStruct=time.localtime(now)
strTime1=time.strftime("%Y-%m-%d",timeStruct)
strTime2=time.strftime("%Y-%m-%d",timeStruct)+" 00:00:00"


os.mkdir("E:/Stock/html_png_Total_day/" + strTime1)

class MyStrategy(strategy.BacktestingStrategy):

    def __init__(self,feed,instrument,smaPeriod):
        super(MyStrategy, self).__init__(feed, 100000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__pricesma=ma.SMA(feed[instrument].getPriceDataSeries(),smaPeriod)
        self.__rsi = rsi.RSI(feed[instrument].getPriceDataSeries(), smaPeriod)
        self.__volsma = ma.SMA(feed[instrument].getVolumeDataSeries(), smaPeriod)
        self.__vol=feed[instrument].getVolumeDataSeries()
        self.__chg = ma.SMA(feed[instrument].getExtraDataSeries(name="pct_chg"), 1)
    def onEnterOk(self, position):
        execInfo=position.getEntryOrder().getExecutionInfo()
        # self.info("Buy at $%.2f" %(execInfo.getPrice()))
        # if str(execInfo.getDateTime())=='2019-09-17 00:00:00':
        #     f.write('\n'+files[x])
        #     f.write(str(execInfo.getDateTime()))

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        # self.info("Sell at $%.2f" % (execInfo.getPrice()))
        self.__position=None
    def getSMA(self):
        return self.__pricesma
    def getsmaVol(self):
        return  self.__volsma
    def getVol(self):
        return self.__vol
    def onBars(self, bars):
#######################################################################################################################
        # if self.__volsma[-1] is None:
        #     return
        # bar=bars[self.__instrument]
        # if self.__position is None:
        #     if bar.getVolume() > (self.__volsma[-1])*2:
        #         shares = int(self.getBroker().getCash() * 0.5 / bars[self.__instrument].getPrice())
        #         self.__position = self.enterLong(self.__instrument, shares, True)
        # elif bar.getVolume() < (self.__volsma[-1]) and not self.__position.exitActive():
        #     self.__position.exitMarket()
        # # elif self.__chg[-1] > 9.8  and not self.__position.exitActive():
        # #     self.__position.exitMarket()
        # # If a position was not opened, check if we should enter a long position.

#------------------------------------------------------------------------------------------
        # if self.__pricesma[-1] is None:
        #     return
        # # print(round(self.__sma[-1],3))
        # bar = bars[self.__instrument]
        # if self.__position is None:
        #     if bar.getPrice() > self.__pricesma[-1]:
        #         shares = int(self.getBroker().getCash() * 0.5 / bars[self.__instrument].getPrice())
        #         # Enter a buy market order for 10 shares. The order is good till canceled.
        #         self.__position = self.enterLong(self.__instrument, shares, True)
        # # Check if we have to exit the position.
        # elif bar.getPrice() < self.__pricesma[-1] and not self.__position.exitActive():
        #     self.__position.exitMarket()
#------------------------------------------------------------------------------------------
        #
        # if self.__volsma[-1] is None:
        #     return
        # bar=bars[self.__instrument]
        # if self.__position is None:
        #     if bar.getVolume() > (self.__volsma[-1])*2:
        #         shares = int(self.getBroker().getCash() * 0.5 / bars[self.__instrument].getPrice())
        #         self.__position = self.enterLong(self.__instrument, shares, True)
        # elif bar.getPrice() < self.__pricesma[-1] and not self.__position.exitActive():
        #     self.__position.exitMarket()

#---------------------------------------------------------------------------------------------

        if self.__volsma[-1] is None:
            return
        bar=bars[self.__instrument]
        if self.__position is None:
            if bar.getPrice() > self.__pricesma[-1] :
                shares = int(self.getBroker().getCash() * 0.5 / bars[self.__instrument].getPrice())
                self.__position = self.enterLong(self.__instrument, shares, True)
                if str(bar.getDateTime()) == strTime2 :
                    # f.write(files[x]+',')
                    # f.write(str(bar.getDateTime())+'\n')
                    s=pd.DataFrame([{'shares_ID':files[x],'trades_date':bar.getDateTime()}])
                    global  df_trade
                    df_trade = pd.concat([s, df_trade], sort=True)
        elif bar.getPrice() < self.__pricesma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()

#--------------------------------------------------------------------
# -------------------------



def run_strategy(smaPeriod):
    global files,x,f,df_trade

    df_new = pd.DataFrame(columns=('shares_ID', 'total number of trades','Profit times number of trades','Profit Percentage','Final portfolio value'))
    df_trade = pd.DataFrame(columns=('shares_ID', 'trades_date'))

    # f = open('E:/Stock/html_png_Total_day/Trade_Today.csv', 'w')
    for (root,dirs,files) in os.walk("E:/Stock/Data_Day"):
        z=0
        for x in range(len(files)):
            z=z+1
            print("进度：", z / len(files) * 100, "%")
            feed = GenericBarFeed(Frequency.DAY,None,None)
            feed.addBarsFromCSV("fd", "E:/Stock/Data_Day/"+files[x])
            myStrategy = MyStrategy(feed, "fd", smaPeriod)
            trade_situation = trades.Trades()
            returnsAnalyzer = returns.Returns()
            myStrategy.attachAnalyzer(trade_situation)
            # plt = plotter.StrategyPlotter(myStrategy)
            # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
            # plt.getInstrumentSubplot("fd").addDataSeries("SMA", myStrategy.getSMA())
            # Plot the simple returns on each bar.
            # plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())
            myStrategy.run()
            # plt.savePlot("E:/Stock/html_png_Total_day/"+files[x]+".png")
            print(files[x]+" Final portfolio value:$%.2f" %myStrategy.getBroker().getEquity())
            print("total number of trades", trade_situation.getCount())
            print("Profit times number of trades ", trade_situation.getProfitableCount())
            # 打印交易次数成功百分比
            if trade_situation.getCount() > 0:
                Percentage = trade_situation.getProfitableCount() / trade_situation.getCount()
            else:
                Percentage = 0
            print("Profit time Percentage", Percentage*100,"%")
            df1= pd.DataFrame({"shares_ID": [files[x]],'total number of trades': [trade_situation.getCount()],'Profit times number of trades' :  trade_situation.getProfitableCount(),'Profit Percentage' : Percentage , 'Final portfolio value': [myStrategy.getBroker().getEquity()]})
            df_new = pd.concat([df1,df_new], ignore_index=True)
    df_new=df_new.sort_values(by='Final portfolio value',ascending=False)
    df_new['Ranking']=range(x+1)
    df_tradable_stocks = df_new[df_new.shares_ID.isin(df_trade.shares_ID)]

    df_new.to_csv("E:/Stock/html_png_Total_day/" + strTime1 + "/"+strTime1+"_Total_Day.csv", index=False)
    df_trade.to_csv("E:/Stock/html_png_Total_day/" + strTime1 + "/"+strTime1+"_Trade_Today.csv")
    df_tradable_stocks.to_csv("E:/Stock/html_png_Total_day/" + strTime1 + "/"+strTime1+"_Today_tradable_stocks.csv")


# i=[240,244,248,252,256,260,264,268,272,276,280,284,288,292,294,298,302]
# for x in i :
run_strategy(18)

#记录结束时间
end = time.perf_counter()
#打印运行时间
print('Running time: %s Seconds'%(end-start))