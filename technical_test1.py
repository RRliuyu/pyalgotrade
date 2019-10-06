from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma
from pyalgotrade.technical import macd
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns, sharpe, drawdown, trades
from pyalgotrade import sma_crossover

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(MyStrategy, self).__init__(feed, 10000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)
        self.__macd=macd.MACD(feed[instrument].getPriceDataSeries(),5,10,8)

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
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 100, True)
        # Check if we have to exit the position.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()

def run_strategy(smaPeriod):
    # Evaluate the strategy with the feed.
    # Load the yahoo feed from the CSV file
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("zggf", "E:/PythonData/CSV/000938.csv")
    myStrategy = MyStrategy(feed, "zggf", smaPeriod)
    myStrategy2 = sma_crossover.SMACrossOver(feed, "zggf", smaPeriod)
    myStrategy3 = macd.(feed,"zggf",5,8,9)
    plt = plotter.StrategyPlotter(myStrategy)
    plt.getInstrumentSubplot("zggf").addDataSeries("SMA", myStrategy2.getSMA())
    plt.getInstrumentSubplot("zggf").addDataSeries("SMA", myStrategy3.getSignal())
    sharpe_ratio = sharpe.SharpeRatio()
    trade_situation = trades.Trades()
    myStrategy.attachAnalyzer(sharpe_ratio)
    myStrategy.attachAnalyzer(trade_situation)
    myStrategy.run()
    print("Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity())
    print("sharpe_ratio", sharpe_ratio.getSharpeRatio(0))
    print("total number of trades", trade_situation.getCount())
    print("Profit times number of trades ", trade_situation.getProfitableCount())
    plt.plot()

run_strategy(20)