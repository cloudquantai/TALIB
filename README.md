# TALIB - The Technical Analysis Library 
## Technical Analysis Library (TA-LIB) for Python Backtesting

Anyone who has ever worked on developing a trading strategy from scratch knows the huge amount of difficulty that is required to get your logic right. You can spend too much time writing code and not enough time getting to a profitable algorithm. CloudQuant has TA-LIB installed on our Python Backtesting to help you develop trading strategies using our historical backtesting simulation and algo development application.

### TA-LIB Turbo-Charges Your Research Loop
TA-Lib is widely used by quantitative researchers and software engineers developing automated trading systems and charts. This freely available tool allows you to gather information on over 200 stock market indicators.

### The Best Part
You don’t need to develop software to find these financial indicators. You can spend your time working with the information to develop trading strategies and not on figuring out how to write code to correctly calculate a formula.
Sample, working scripts that demonstrate how to use TA-LIB in app.CloudQuant.com

### What’s included in TA-LIB?
Several categories of Technical Analysis are included and relatively easy to use. The categories are as follows:

**Overlap Studies.** The overlap studies cover data typically used in common “overlays” to stock market charts. The most common of these are the moving averages and trendlines.

**Momentum Indicators.** Indicators for the speed or velocity of a price change in each security. This is easily thought of as a measurement of the rate of change (increase/decrease) in the market price of the security.

**Volume Indicators.** Volume is the quantity of a security that has been traded in the specified time (day, hour, minute, …). Volume can be used to judge the strength or weakness of a market move.

**Volatility Indicators.** Volatility is the amount of dispersion or fluctuation in the price of a security. Volatility indicators are useful for determining the amount of risk or potential profit that exists in the security. The volatility indicators in TA-LIB can be thought of as “Range” indicators.

**Price Transform.** Statistical information about how a price is changing (average, median, …)

**Cycle Indicators.** Cycle Indicators are used by technical analysts to analyze variations in the amplitude of securities. These are commonly called Hilbert Transform Price Cycles.

**Pattern Recognition.** Charting patterns have been around for a very long time. They go by many names including Japanese Candlesticks. Chart patterns look at the overall market typically assuming the market price is the best indicator of all other statistics. The patterns that are found in stock charts give a technical analyst an indicator of likely future changes.

### You Can Get Started with TA-LIB Rather Easily
In the CloudQuant public Scripts directory (or alternatively on our Github) you can find the demo python code that we used in our introduction video.

There are a few skills that you will need. At some point, you need to become familiar with NUMPY. For now, simply copy our code to get your technical indicators.

#### Getting Started
Setup your script with importing the two things you need. Add the following two lines to the top of your python script. This simply tells python that you will be using TALIB and NUMPY.

```python
import talib
import numpy
```

#### Now Get Market Data to Analyze
In our CloudQuant environment, we do this by adding the following line of code. In this example, we are pulling down the preceding 30 days of market data.

```python
daily_bars = md.bar.daily(start=-30,include_empty=False)
```

#### Make it simple by putting your data into single variable
The daily bars are an object that has more data than we really need. To make things simple we are going to place the closing prices into a simple list variable.

```python
close = daily_bars.close
``` 

This gives us the 30 days of closing prices into our “close” variable and will make it very easy to work with TA-LIB.

#### Let’s Use TA-LIB to Calculate Relative Strength Index
Now that we have our 30 days of closing prices we can now calculate the Relative Strength Index. The relative strength index (RSI) is a momentum used to measure the extent of price gains and losses over a set timeframe. Technical analysts use this indicator to identify potentially overbought or oversold securities.

The next step of our code is to call the RSI function in the TA-LIB to get the RSI

```python
RSI = talib.RSI(close, timeperiod=14)
print RSI
```

This code says that we want to calculate the Relative Strength Index for 14 (days) and then print it out.

#### Here’s the Output – in an ordered list
The output comes back to you in an ordered list. The first 14 values are “nan.” Nan is python’s way of telling you it has no value for that item. We get 14 nans because we told the RSI to use 14 time periods!

```
[         nan          nan          nan          nan          nan
        nan          nan          nan          nan          nan
          nan          nan          nan          nan  64.05692275
  63.08980305  69.90074285  70.56622216  72.52847877  71.8946513
  73.32911372  53.32483143  59.01449969  55.30032544  46.7538174
  47.24702886  50.6444966   53.09614359  56.16268149  61.00753914]
```

To print out the latest RSI you can use the following line:

```python
print RSI[-1]
```

### We promise to help you with TA-LIB
Support for TA-LIB in CloudQuant is available in the [Technical Analysis section of our community forums.](https://forum.cloudquant.com/categories/technical-analysis) If you have a question please post it there so we can help you in your trading strategy research. Keep in mind, if you have the question then someone else probably does too.
