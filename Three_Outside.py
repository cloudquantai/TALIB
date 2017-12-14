from cloudquant.interfaces import Strategy
from collections import OrderedDict
import ktgfunc
import numpy
import talib

#######################################################################################
# This script demonstrates using TA-LIB for the trading signal discussed in this blog:
# https://info.cloudquant.com/2017/11/tk-bullish-turn-of-events/
#
# This script works in the app.cloudquant.com environment.
#
#


class DEMO_THREE_OUTSIDE(Strategy):

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        days=len(md.bar.daily(start=-100,include_empty=False).close) # request 100 close prices, get the length of what we got back.
        return days>20 and md.stat.avol>200000 # more than 20 trading days data on file and average vol over 200k and the model will run for this symbol

    def on_start(self, md, order, service, account):

        # Needs only 4 days of data to detect a Three Outside signal.
        # So most of the time you will just want to know if a symbol triggered yesterday so 4 bars is enough
        # grab more bars and uncomment the extra code to look for older signals or repeat signals
        
        daily_bars = md.bar.daily(start=-4,include_empty=False) 
        close = daily_bars.close # close bars
        high = daily_bars.high   # high bars
        low = daily_bars.low     # low bars
        open = daily_bars.open   # open bars
        talib_nump = talib.CDL3OUTSIDE(open, high, low, close) # call returns a numpy array of either -100 or 0 or 100
        talib_list = numpy.ndarray.tolist(talib_nump) # if you prefer you can convert it to a normal list
        print self.symbol,talib_list #,talib_list.index(100) # finds the location of the FIRST 100 entry in the list
        if abs(talib_nump[-1])==100: # If it is 100 or -100 then ALERT!
            print "True Yesterday",self.symbol
#        elif max(talib_nump)==100:
#            print "True during test period",self.symbol,numpy.where(talib_nump) # Finds location of all non-zero entries in the array
#            print self.symbol,talib_list,talib_list.index(100) # finds the location of the FIRST 100 entry in the list and the FIRST -100 entry
#        elif min(talib_nump)==-100:
#            print "True during test period",self.symbol,numpy.where(talib_nump) # Finds location of all non-zero entries in the array
#            print self.symbol,talib_list,talib_list.index(-100) # finds the location of the FIRST 100 entry in the list and the FIRST -100 entry
        
        


    
