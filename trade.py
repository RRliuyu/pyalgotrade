from pyalgotrade import strategy
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from pyalgotrade.stratanalyzer import trades
from pyalgotrade.broker import Broker
import pandas as pd
import os
import csv
import datetime
from pyalgotrade import plotter
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self,feed,instrument,smaPeriod):
        super(MyStrategy, self).__init__(feed, 1000000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        # self.setUseAdjustedValues(True)
        self.__sma=ma.SMA(feed[instrument].getPriceDataSeries(),smaPeriod)
        self.__rsi = rsi.RSI(feed[instrument].getPriceDataSeries(), smaPeriod)
        self.__volsma = ma.SMA(feed[instrument].getVolumeDataSeries(), smaPeriod)
        self.__vol=feed[instrument].getVolumeDataSeries()
        self.__chg = ma.SMA(feed[instrument].getExtraDataSeries(name="pct_chg"), 1)
        self.__buyday = self.getCurrentDateTime()
    def onEnterOk(self, position):
        execInfo=position.getEntryOrder().getExecutionInfo()
        self.info("Buy at $%.2f" %(execInfo.getPrice()))
    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("Sell at $%.2f" % (execInfo.getPrice()))
        self.__position=None
    def getSMA(self):
        return self.__sma
    def getsmaVol(self):
        return  self.__volsma
    def getVol(self):
        return self.__vol
    def getBuyday(self):
        return self.__buyday
    def onBars(self, bars):
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
        if self.__sma[-1] is None:
            return
        bar = bars[self.__instrument]
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                shares = int(self.getBroker().getCash() * 0.2 / bars[self.__instrument].getPrice())
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
                buyday = self.getCurrentDateTime()+datetime.timedelta(days=1)
                print(buyday)

        # Check if we have to exit the position.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()
def run_strategy(smaPeriod):
    df_new = pd.DataFrame(columns=('shares_ID', 'total number of trades','Profit times number of trades','Profit Percentage','Final portfolio value'))
    for (root,dirs,files) in os.walk("E:/SHZQ"):
        for x in range(len(files)):
            feed = GenericBarFeed(Frequency.WEEK,None,None)
            feed.addBarsFromCSV("fd", "E:/SHZQ/"+files[x])
            myStrategy = MyStrategy(feed, "fd", smaPeriod)
            trade_situation = trades.Trades()
            myStrategy.attachAnalyzer(trade_situation)
            myStrategy.run()
            print(files[x]+"Final portfolio value:$%.2f" %myStrategy.getBroker().getEquity())
            print("total number of trades", trade_situation.getCount())
            print("Profit times number of trades ", trade_situation.getProfitableCount())
            if trade_situation.getCount() > 0:
                Percentage = trade_situation.getProfitableCount() / trade_situation.getCount()
                print("百分比",Percentage)
            else:
                Percentage = 0
                print("百分比", 0)
            df1= pd.DataFrame({"shares_ID": [files[x]],'total number of trades': [trade_situation.getCount()],'Profit times number of trades' :  trade_situation.getProfitableCount(),'Profit Percentage' : Percentage , 'Final portfolio value': [myStrategy.getBroker().getEquity()]})
            df_new = pd.concat([df1,df_new], ignore_index=True)
    df_new.to_csv("E:/Stock/html_png_Total//Total.csv", index=False)


run_strategy(18)