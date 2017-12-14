from cloudquant.interfaces import Strategy
import talib
import numpy

#####################################################################
# Technical Analysis Library (TA-LIB) for Python Backtesting
# Intro / demo Script for use in app.CloudQuant.com


class TALIB_DEMO(Strategy):

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
#        return symbol=="SPY"
        sp500=service.symbol_list.in_list(service.symbol_list.get_handle('9a802d98-a2d7-4326-af64-cea18f8b5d61'),symbol)   # list.in_list ( sp500 list for today, current symbol)
        return symbol== 'SPY' or sp500
    
    def on_start(self, md, order, service, account):
        print self.symbol
        
        # First we need some historic data so lets grab 30 daily bars
        daily_bars = md.bar.daily(start=-30,include_empty=False) 

        # most TALIB calls use OHLC (Open, High, Low, Close) in some form so lets pull those out so we have them ready
        open = daily_bars.open   
        high = daily_bars.high   
        low = daily_bars.low     
        close = daily_bars.close 
        volume = daily_bars.volume

        # now lets do a few TALIB calls and see what we get back

        # TALIB calls return numpy arrays, you can use numpy.ndarray.tolist() to convert to a normal list
        # These numpy arrays can contain floats such as a moving average price day to day
        # or they can contain a signal, often a series of zeros with 100 (and sometimes -100) indicating a signal
        # if there is insufficient data to return a result or a signal you will get a NAN
        # so for a 10 period moving average your first 9 entries will be NANs, the 10th will be your first Moving Average

        
        
        # TALIB.CDLENGULFING
        # returns a pandas array containing -100 for an engulfing red bar and 100 for an engulfing green bar.
        # CDLENGULFING is for the body of the candle only, not the wicks....
        engulf = talib.CDLENGULFING(open, high, low, close) # call returns a numpy array of either 0 or 100
        engulflist = numpy.ndarray.tolist(engulf) # if you prefer you can convert it to a normal list
#        print "Engulf Numpy",engulf
        print "Engulf List",engulflist
        
        if engulf[-1]==100:
            print "Yesterday Engulfed the previous day - Bullish (green bar) ********"
        elif engulf[-1]==-100:
            print "Yesterday Engulfed the previous day - Bearish (red bar)   ********"
                                                        

        # TALIB.RSI
        RSI = talib.RSI(close, timeperiod=14)
        RSIlist = numpy.ndarray.tolist(RSI)
#        print "RSI Numpy",RSI
        print "RSI List (Last 10 entries)",RSIlist[-10:]

        # TALIB.CDL3OUTSIDE
        # trend has a direction, oldest of three bars has the same direction, second bar consumes first bar and has opposite direction, third bar continues this direction
        ThreeOut = talib.CDL3OUTSIDE(open, high, low, close)
        ThreeOutlist = numpy.ndarray.tolist(ThreeOut)
#        print "ThreeOutside Numpy",ThreeOut
        print "ThreeOutside List",ThreeOutlist
        if abs(ThreeOut[-1])==100:
            print "Three Outside Yesterday",self.symbol


        # TALIB.ADX if you put in 10, then your 20th data item will have a result.
        ADX = talib.ADX(high, low, close,timeperiod=14)
        MINUS_DI = talib.MINUS_DI(high, low, close,timeperiod=14) 
        PLUS_DI = talib.PLUS_DI(high, low, close,timeperiod=14) 
        ADXlist = numpy.ndarray.tolist(ADX) 
        MINUS_DI_list = numpy.ndarray.tolist(MINUS_DI)
        PLUS_DI_list = numpy.ndarray.tolist(PLUS_DI) 

        print "ADX List (last 10 entries)",ADXlist[-10:]
        print "MINUS_DI List (last 3 entries)",MINUS_DI_list[-3:]
        print "PLUS_DI list (last 3 entries)",PLUS_DI_list[-3:]

#        if (ADX[-1] > 40.0) and (ADX[-2] < 40.0) and (PLUS_DI[-1] > MINUS_DI[-1]):
        if ADX[-1] > 50.0 and (PLUS_DI[-1] > MINUS_DI[-1]):
            print self.symbol,"Go Long   ", ADX[-1], ADX[-2], PLUS_DI[-1], MINUS_DI[-1]
#        elif (ADX[-1] > 40.0) and (ADX[-2] < 40.0) and (PLUS_DI[-1] < MINUS_DI[-1]):
        elif ADX[-1] > 50.0 and (PLUS_DI[-1] < MINUS_DI[-1]):
            print self.symbol,"Go Short  ", ADX[-1] ,ADX[-2], PLUS_DI[-1], MINUS_DI[-1]

        # TALIB.MA - Moving Average - matype=0 by default...
        # 0 = SMA (Simple Moving Average) (Default)
        # 1 = EMA (Exponential Moving Average)
        # 2 = WMA (Weighted Moving Average)
        # 3 = DEMA (Double Exponential Moving Average)
        # 4 = TEMA (Triple Exponential Moving Average)
        # 5 = TRIMA (Triangular Moving Average)
        # 6 = KAMA (Kaufman Adaptive Moving Average)
        # 7 = MAMA (MESA Adaptive Moving Average)
        # 8 = T3 (Triple Exponential Moving Average)            
            
        SMA = talib.MA(close,timeperiod=20)
        SMAlist = numpy.ndarray.tolist(SMA) 
        print "Simple Moving Average",SMAlist

        EMA = talib.MA(close,timeperiod=20,matype=1)
        EMAlist = numpy.ndarray.tolist(EMA) 
        print "Exponential Moving Average",EMAlist
        
        print "Simple Moving Average      (last 3 entries)",SMAlist[-3:]
        print "Exponential Moving Average (last 3 entries)",EMAlist[-3:]
        print "Average of last 20 close prices",sum(close[-20:])/len(close[-20:])
        print "Last Three close prices...", close[-3:]
        print
        service.terminate()
        return 

#            if engulf[-1]==100:
#                print "Bearish Engulf yesterday",self.symbol
#        else:
#                print "Bullish Engulf yesterday",self.symbol
#        elif max(engulf)==100:
#            print engulflist,engulflist.index(100) # finds the location of the FIRST 100 entry in the list
#            print engulflist,engulflist[::-1].index(100) # finds the location of the LAST 100 entry ie the most recent.. the one we want!
#        elif min(engulf)==-100:
#            print engulflist,engulflist.index(-100) # finds the location of the FIRST -100 entry in the list
#            print engulflist,engulflist[::-1].index(-100) # finds the location of the LAST -100 entry ie the most recent.. the one we want!

#        service.terminate()