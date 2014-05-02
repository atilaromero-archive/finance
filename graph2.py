#!/usr/bin/env python
import sys
import pylab
import stats
import matplotlib
import numpy

from utils import *

def main():
    sp=getquotes('PETR4.SA',
                 2009,1,1,
                 2014,2,28)
    def plotidx(idx,**kargs):
        pylab.plot_date(sp.date[1:],idx,"-",**kargs)

    #stats.plotreturnshist(percentvar(sp.close)*numpy.log(sp.volume[1:]+1))
    """
    for x in range(2008,2014):
        sp=getquotes('PETR3.SA',
                     x  ,1,1,
                     x+1,1,1)
        stats.plotreturnsxvarvolume(sp,label=str(x))
    """

    
    #plotidx(obv.obv(sp.close,sp.volume)/10000000,'obv close')
    #plotidx(obv.retxvol(sp.close,sp.volume)/1000000,"retxvol")
    #plotidx(obv.retxvarvol(sp.close,sp.volume)/1000000,'retxvarvol')
    plotidx(sp.close[1:],label='close')
    
    ax = plt.gca()
    ax.set_yscale('log')
    
    #matplotlib.finance.candlestick(ax,sp)

    pylab.grid(b=True, which='major', color='b', linestyle='-')
    pylab.rcParams['legend.loc'] = 'best'
    pylab.legend()
    pylab.show()

if __name__ == '__main__':
    main(*sys.argv[1:])
