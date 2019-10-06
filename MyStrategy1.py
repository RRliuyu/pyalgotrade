from pyalgotrade import strategy
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from pyalgotrade.stratanalyzer import trades
import os
from pyalgotrade.broker import Broker

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self,feed,instrument,smaPeriod,factor1):
        super(MyStrategy, self).__init__(feed, 1000000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__sma=ma.SMA(feed[instrument].getPriceDataSeries(),smaPeriod)
        self.__rsi = rsi.RSI(feed[instrument].getPriceDataSeries(), smaPeriod)
        self.__volsma = ma.SMA(feed[instrument].getVolumeDataSeries(), smaPeriod)
        self.__vol=feed[instrument].getVolumeDataSeries()
        self.__chg = ma.SMA(feed[instrument].getExtraDataSeries(name="pct_chg"), 1)
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
    def onBars(self, bars):
        if self.__volsma[-1] is None:
            return
        bar=bars[self.__instrument]
        if self.__position is None:
            if bar.getVolume() > (self.__volsma[-1])*2:
                shares=int(self.getBroker().getCash()/bars[self.__instrument].getPrice())
                self.__position=self.enterLong(self.__instrument,shares,True)
        # elif bar.getVolume() < (self.__volsma[-1]) and not self.__position.exitActive():
        #     self.__position.exitMarket()
        elif self.__chg[-1] > 9.8  and not self.__position.exitActive():
            self.__position.exitMarket()
            print(self.__chg[-1] )

def run_strategy(smaPeriod,factor1):
    import pandas as pd
    # df_new = pd.DataFrame(columns=('shares_ID', 'total number of trades','Profit times number of trades','Final portfolio value'))
    for (root,dirs,files) in os.walk("E:/SHZQ"):
        for x in range(len(files)):
            feed = GenericBarFeed(Frequency.DAY,None,None)
            feed.addBarsFromCSV("fd", "E:/SHZQ/"+files[x])

            myStrategy = MyStrategy(feed, "fd", smaPeriod,factor1)
            trade_situation = trades.Trades()
            myStrategy.attachAnalyzer(trade_situation)
            myStrategy.run()
            print(files[x]+"Final portfolio value:$%.2f" %myStrategy.getBroker().getEquity())
            print("total number of trades", trade_situation.getCount())
            print("Profit times number of trades ", trade_situation.getProfitableCount())
            print("百分比",trade_situation.getProfitableCount()/trade_situation.getCount())
            print(trade_situation.getCount())
            df1= pd.DataFrame({"shares_ID": [files[x]],'total number of trades': [trade_situation.getCount()],'Profit times number of trades' :  trade_situation.getProfitableCount(),'Final portfolio value': [myStrategy.getBroker().getEquity()]})
    #         df_new = pd.concat([df1,df_new], ignore_index=True)
    # df_new.to_csv("E:/PythonData/CSV/testTotal.csv", index=False, )