from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import ma
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns, sharpe, drawdown, trades


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(MyStrategy, self).__init__(feed, 10000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)
        self.Sma_price = []

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        bar = bars[self.__instrument]
        self.Sma_price.append(self.__sma[-1])
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                print("buy", bar.getDateTime(), self.__sma[-1], bar.getPrice())
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 100, True)
        # Check if we have to exit the position.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            print("sell", bar.getDateTime(), self.__sma[-1], bar.getPrice())
            self.__position.exitMarket()

def run_strategy(smaPeriod):
    # Load the yahoo feed from the CSV file
    # feed = yahoofeed.Feed()
    feed = GenericBarFeed(Frequency.DAY, None, None)
    feed.addBarsFromCSV("zggf", "E:\Stock\Data_Day/000831.SZ.csv")
    global myStrategy
    # Evaluate the strategy with the feed.
    myStrategy = MyStrategy(feed, "zggf", smaPeriod)
    plt = plotter.StrategyPlotter(myStrategy)
    sharpe_ratio = sharpe.SharpeRatio()
    trade_situation = trades.Trades()
    myStrategy.attachAnalyzer(sharpe_ratio)
    myStrategy.attachAnalyzer(trade_situation)
    myStrategy.run()
    print ("Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity())
    print("sharpe_ratio", sharpe_ratio.getSharpeRatio(0))
    print("total number of trades", trade_situation.getCount())
    print("Profit times number of trades ", trade_situation.getProfitableCount())
    print(myStrategy.Sma_price)
    plt.plot()


run_strategy(18)

