from cloudquant.interfaces import Strategy
from collections import OrderedDict
import ktgfunc
import numpy
import talib


#######################################################################################
# This script demonstrates using TA-LIB for the trading signal discussed in this blog:
# https://info.cloudquant.com/2017/12/catalent-inc-ctlt-bearish-engulfing-sell-signal/
#
# This script works in the app.cloudquant.com environment.
#
#


class DEMO_Engulf(Strategy):

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        days=len(md.bar.daily(start=-100,include_empty=False).close) # request 100 close prices, get the length of what we got back.
        return days>20 and md.stat.avol>200000 # more than 20 trading days data on file and average vol over 200k and the model will run for this symbol

    def on_start(self, md, order, service, account):

        # returns a pandas array containing -100 for an engulfing red bar and 100 for an engulfing green bar.
        # engulf appears to be for the body of the candle only, not the wicks....

        daily_bars = md.bar.daily(start=-11,include_empty=False) # grab 11 bars of historical data
        close = daily_bars.close # close bars
        high = daily_bars.high   # high bars
        low = daily_bars.low     # low bars
        open = daily_bars.open   # open bars

        # lets only look at symbols that have 11 daily bars (no IPOs or recent splits)        
        if len(daily_bars.open) == 11:
            engulf = talib.CDLENGULFING(open, high, low, close) # call returns a numpy array of either 0 or 100
            engulflist = numpy.ndarray.tolist(engulf) # if you prefer you can convert it to a normal list
            
            # yesterday (-1) engulfed the day before (-2) so we want to know what the trend was for the previous 10 bars -11 to -2
            pctMove = round(((close[-2]-close[-11])/close[-2])*100,1)
            
            if engulf[-1]==100 and pctMove<-1.0 and pctMove>-5.0:
                print self.symbol.ljust(6)," Bullish Engulf : Green Engulf Bar and previous 10 day trend was down more than 5%",
                print engulf[-1],"previous 10 day move",round(((close[-2]-close[-11])/close[-2])*100,1),"%, ",round(close[-2]-close[-11],2),"old close",round(close[-11],2),"close before engulf",round(close[-2],2)
                order.algo_buy(self.symbol, algorithm="arca_moo_buy", intent="init",order_quantity=100)
                order.algo_sell(self.symbol, algorithm="arca_moc_sell", intent="none",order_quantity=100)                

            if engulf[-1]==-100 and pctMove>1.0 and pctMove<5.0:
                print self.symbol," Bearish Engulf : Red   Engulf Bar and previous 10 day trend was up   more than 5%",
                print engulf[-1],"previous 10 day move",round(((close[-2]-close[-11])/close[-2])*100,1),"%, ",round(close[-2]-close[-11],2),"old close",round(close[-11],2),"close before engulf",round(close[-2],2)
                order.algo_sell(self.symbol, algorithm="arca_moo_sell", intent="init",order_quantity=100)
                order.algo_buy(self.symbol, algorithm="arca_moc_buy", intent="none",order_quantity=100)                
            
#            if max(engulf)==100:
#                print engulflist,engulflist.index(100) # finds the location of the FIRST 100 entry in the list
#                print engulflist,engulflist[::-1].index(100) # finds the location of the LAST 100 entry ie the most recent.. the one we want!
#            if min(engulf)==-100:
#                print engulflist,engulflist.index(-100) # finds the location of the FIRST -100 entry in the list
#                print engulflist,engulflist[::-1].index(-100) # finds the location of the LAST -100 entry ie the most recent.. the one we want!
            
#        service.terminate()