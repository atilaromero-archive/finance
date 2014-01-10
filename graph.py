#!/usr/bin/env python
import sys
import pylab
import functools
import matplotlib
import datetime
import numpy

def _apply(f):
    def _g(g):
        @functools.wraps(g)
        def _f(*args, **kwds):
            return f(g(*args,**kwds))
        return _f
    return _g

@_apply(list)
def integral(array):
    acc=0
    for x in array:
        acc+=x
        yield acc

def percentvar(prices):
    return (prices[1:]-prices[:-1])/prices[1:]

def var(prices):
    return (prices[1:]-prices[:-1])

def normalize(array):
    maxidx=max(max(array),-min(array))
    return array/maxidx

def obv(price,volume):
    dprice=var(price)
    idx=((dprice>0)*1+(dprice<0)*(-1))*volume[1:]
    return idx.cumsum()

def retxvol(price,volume):
    idx=percentvar(price)*volume[1:]
    return idx.cumsum()

def retxvarvol(price,volume):
    idx=percentvar(price)*var(volume)
    return idx.cumsum()

def plothist(returns):
    n,bins,patches=pylab.hist(returns,100)
    mu=numpy.mean(returns)
    sigma = numpy.std(returns)
    x = matplotlib.mlab.normpdf(bins, mu, sigma)
    #pylab.plot(bins, x, color='red')
    pylab.show()

def main():
    date1 = datetime.date( 2012, 1, 1 )
    date2 = datetime.date( 2014, 1, 6 )
    sp= matplotlib.finance.quotes_historical_yahoo('PETR3.SA',date1,date2,asobject=True)
    sp=sp[sp.volume>0]
    def plotidx(idx,label=None):
        pylab.plot_date(sp.date[1:],idx,"-",label=label)


    #plothist(percentvar(sp.close)*numpy.log(sp.volume[1:]+1))
    #plotidx(integral(percentvar(sp.open)*var(sp.volume)/100000))
    #plotidx(integral(percentvar(sp.close)*var(sp.volume)/100000))

    """
    plotidx(retxvol(sp.close,sp.volume)/1000000,"retxvol")
    plotidx(retxvarvol(sp.close,sp.volume)/1000000,'retxvarvol')
    plotidx(obv(sp.close,sp.volume)/10000000,'obv close')
    plotidx(obv(sp.open,sp.volume)/10000000,'obv open')
    plotidx(obv(sp.open+sp.close,sp.volume)/10000000,'obv o+c')
    plotidx(sp.close[1:],'close')
    """

    pylab.plot(sp.close,sp.volume,".")

    pylab.grid(b=True, which='major', color='b', linestyle='-')
    pylab.rcParams['legend.loc'] = 'best'
    pylab.legend()
    pylab.show()

if __name__ == '__main__':
    main(*sys.argv[1:])
