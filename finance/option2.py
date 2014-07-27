#!/usr/bin/python
import datetime
import pylab
import numpy as np
import blackscholes as bs
import collections

class Money(object):
    @staticmethod
    def value(*args, **kwargs):
        return 1

class Option(object):
    def __init__(self, strikeprice, expirationdate, optype):
        self.strikeprice = strikeprice
        if not isinstance(expirationdate, datetime.date):
            expirationdate = datetime.date(*expirationdate)
        self.expirationdate = expirationdate
        self.optype = optype

    def value(self, stockprice, date=None, volatility=0.020, rate=0.00018):
        if date == None:
            date = datetime.date.today()
        daystoexp = (self.expirationdate - date).days
        if daystoexp < 0:  
            return 0
            #daystoexp = 0 
        return bs.BlackScholes(self.optype,stockprice,self.strikeprice,daystoexp,rate,volatility)

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
        for leg in legs:
            self[leg.asset] += leg.quantity
        self.date = date
        if hasattr(self,'pricerange'):
            self.plot(self.pricerange)

    def autoplot(self, pricerange):
        self.pricerange = pricerange

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
        self.tradehistory.append((legs, date))
        self.balance.append(legs, date)
        self.balancehistory.append(self.balance.snapshot())

    def cash(self, quantity, date=None):
        self._updatebalance([Leg(Money, quantity)], date)

    def trade(self, option, quantity, price=None, date=None, stockprice=None):
        if price == None:
            price = option.value(stockprice, date)
        commission = 0 # TODO
        self._updatebalance([Leg(option, quantity), 
                             Leg(Money, -(price*quantity)), 
                             Leg(Money, -commission)], date)

        
