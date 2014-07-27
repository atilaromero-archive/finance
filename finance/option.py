#!/usr/bin/python
import datetime
import pylab
import numpy as np
import blackscholes as bs
import collections

def _preparedate(date):
    if isinstance(date, tuple) or isinstance(date, list):
        date = datetime.date(*date)
    return date

class Money(object):
    @staticmethod
    def value(*args, **kwargs):
        return 1

class Option(object):
    def __init__(self, strikeprice, expirationdate, optype):
        self.strikeprice = strikeprice
        expirationdate = _preparedate(expirationdate)
        self.expirationdate = expirationdate
        self.optype = optype

    def value(self, stockprice, date=None, volatility=0.020, rate=0.00018):
        if date == None:
            date = datetime.date.today()
        daystoexp = (self.expirationdate - date).days
        if daystoexp < 0:  
            return 0
            #daystoexp = 0 
        result = bs.BlackScholes(self.optype,0.0+stockprice,self.strikeprice,daystoexp,rate,volatility)
        return result

    def __repr__(self):
        return '<{0}, {1}, {2}>'.format(self.__class__.__name__, self.expirationdate, self.strikeprice)

class Call(Option):
    def __init__(self, strikeprice, expirationdate):
        super(Call, self).__init__(strikeprice, expirationdate, 'c')

class Put(Option):
    def __init__(self, strikeprice, expirationdate):
        super(Put, self).__init__(strikeprice, expirationdate, 'p')

Leg = collections.namedtuple('Leg', ('asset', 'quantity'))

class Balance(collections.defaultdict):
    def __init__(self, *args, **kwargs):
        super(Balance, self).__init__(lambda : 0, *args, **kwargs)
        self.default_factory = lambda : 0

    def append(self, legs, date):
        date = _preparedate(date)
        for leg in legs:
            self[leg.asset] = round(self[leg.asset] + leg.quantity, 2)
        self.date = date

    def snapshot(self):
        result =  Balance(dict([(k,v) for k, v in self.iteritems() if v != 0]))
        result.date = self.date
        return result

    def plot(self, pricerange, **kwargs):
        result = 0 * pricerange
        for asset, quantity in self.iteritems():
            result += quantity * asset.value(pricerange, self.date)
        pylab.plot(pricerange, result, **kwargs)

class History:
    def __init__(self):
        self.tradehistory = []
        self.balance = Balance()
        self.balancehistory = []

    def _updatebalance(self, legs, date):
        date = _preparedate(date)
        self.tradehistory.append((legs, date))
        self.balance.append(legs, date)
        self.balancehistory.append(self.balance.snapshot())

    def cash(self, quantity, date=None):
        date = _preparedate(date)
        self._updatebalance([Leg(Money, quantity)], date)

    
    @staticmethod
    def commission(price, quantity):
        result = 0
        for percent in [0.04, 0.03, 0.07]:
            result += np.trunc(percent * price * quantity)
        result += np.trunc(7.5 * 105.0)
        return float(result) / 100.0
        
    def trade(self, option, quantity, price=None, date=None, stockprice=None):
        date = _preparedate(date)
        if price == None:
            price = option.value(stockprice, date)
        commission = self.commission(price, quantity)
        self._updatebalance([Leg(option, quantity), 
                             Leg(Money, -round(price*quantity, 2)), 
                             Leg(Money, -commission)], date)

    def plotAll(self, pricerange):
        for b in self.balancehistory:
            b.plot(pricerange)
        pylab.show()
