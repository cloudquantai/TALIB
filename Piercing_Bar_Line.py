from cloudquant.interfaces import Strategy
from collections import OrderedDict
import ktgfunc
import numpy
import talib


#######################################################################################
# This script demonstrates using TA-LIB for the trading signal discussed in this blog:
# https://info.cloudquant.com/2017/11/tk-piercing-line/
#
# This script works in the app.cloudquant.com environment.
#
#



class DEMO_PIERCING(Strategy):

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        days=len(md.bar.daily(start=-100,include_empty=False).close) # request 100 close prices, get the length of what we got back.
        return days>20 and md.stat.avol>200000 # more than 20 trading days data on file and average vol over 200k and the model will run for this symbol

    def on_start(self, md, order, service, account):

        # Needs 10 days of data before the two bars for the pierce to confirm a downtrend.
        # Therefor minimim bars pull is 12 which will tell you if you had a pierce yesterday

        daily_bars = md.bar.daily(start=-20,include_empty=False) # grab 20 bars of historical data
        close = daily_bars.close # close bars
        high = daily_bars.high   # high bars
        low = daily_bars.low     # low bars
        open = daily_bars.open   # open bars
        pierce = talib.CDLPIERCING(open, high, low, close) # call returns a numpy array of either 0 or 100
        piercelist = numpy.ndarray.tolist(pierce) # if you prefer you can convert it to a normal list
        if pierce[-1]==100:
            print "Pierced yesterday",self.symbol
        elif max(pierce)==100:
            print "Pierced during test period",self.symbol,numpy.where(pierce) # Finds location of all non-zero entries in the array
            print piercelist,piercelist.index(100) # finds the location of the FIRST 100 entry in the list
