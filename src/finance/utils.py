#!/usr/bin/python
import functools
import datetime
import matplotlib

def getquotes(name,y1,m1,d1,y2,m2,d2):
    date1 = datetime.date( y1, m1, d1 )
    date2 = datetime.date( y2, m2, d2 )
    sp=matplotlib.finance.quotes_historical_yahoo(name,date1,date2,asobject=True)
    sp=sp[sp['volume']>0]
    return sp

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

def normalize(array):
    maxidx=max(max(array),-min(array))
    return array/maxidx

