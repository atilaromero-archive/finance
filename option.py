#!/usr/bin/python
import datetime
import pylab
import numpy as np
import blackscholes as bs

class Option:
    rate=0.00018
    volatility=0.015
    def __add__(self,y):
        ret=Option()
        ret.value= self.value+y.value
        assert np.all(self.prices==y.prices)
        ret.prices=self.prices
        return ret
    
    def __sub__(self,y):
        ret=Option()
        ret.value= self.value-y.value
        assert np.all(self.prices==y.prices)
        ret.prices=self.prices
        return ret

    def plot(self,*args,**kwargs):
        pylab.plot(self.prices,self.value,*args,**kwargs)   

    def plotDelta(self,*args,**kwargs):
        dx=self.prices[1:]-self.prices[:-1]
        dy=self.value[1:] - self.value[:-1]
        x=self.prices[:-1]
        y=self.value[:-1]
        pylab.plot(x,(dy/dx)/y,*args,**kwargs)   

class Call(Option):
    def __init__(self,precoexercicio,precoacao,daystoexp):
        self.prices=precoacao
        self.value=bs.BlackScholes('c',precoacao,precoexercicio,daystoexp,Option.rate,Option.volatility)

class Put(Option):
    def __init__(self,precoexercicio,precoacao,daystoexp):
        self.prices=precoacao
        self.value=bs.BlackScholes('p',precoacao,precoexercicio,daystoexp,Option.rate,Option.volatility)

def plotspread(exercicio1,exercicio2,daystoexp,min=12,max=20):
    price=np.arange(min,max,0.005)
    option1=Call(exercicio1,price,daystoexp)
    option2=Call(exercicio2,price,daystoexp)
    opt=option1-option2
    pylab.plot(price,opt.value,'-',label='%s:%s:%s'%(exercicio1,exercicio2,daystoexp))

def t1():
    price=np.arange(16,20,0.005)
    ex=16
    d=(datetime.date(2014,06,16)-datetime.date.today()).days
    a=Put(16.66,price,d)
    b=Call(19.16,price,d)
    a.plot('-')
    b.plot('-')
    for x in [-1.5,-1,-0.5,0,0.5,1,1.5]:
        a=Put(18.16-x,price,d)
        b=Call(18.16+x,price,d)
        c=a+b
        c.value=c.value/min(c.value)
        c.plot('-',label=str(x))

def t2():
    price=np.arange(16,20,0.005)
    ex=18
    d=(datetime.date(2014,06,16)-datetime.date.today()).days
    for v in np.arange(0.01,0.03,0.005):
        Option.volatility=v
        #a=Put(16.66,price,d)
        b=Call(19.16,price,d)
        b.plot('-',label=str(v))

def t3():
    price=np.arange(16,20,0.005)
    for d in [10,30]:
        for v in np.arange(0.02,0.0205,0.005):
            Option.volatility=v
            a=Call(16.66,price,d)
            b=Call(18.66,price,d)
            c=a-b
            c.plot('-',label='c'+str(v)+str(d))
            a.plot('-',label='a'+str(v)+str(d))

def t4():
    price=np.arange(10,25,0.005)
    for d in [0,30]:
        for v in [0.02]:
            Option.volatility=v
            a=Call(16.66,price,d)
            b=Put(16.66,price,d)
            c=a+b
            c.plot('-',label='c'+str(v)+str(d))
            #a.plot('-',label='a'+str(v)+str(d))
    c.plotDelta('-',label='delta c'+str(v)+str(d))
    #a.plotDelta('-',label='delta a'+str(v)+str(d))

if __name__=="__main__":
    t4()
    ax = pylab.plt.gca()
    #ax.set_xscale('log')
    #ax.set_yscale('log')
    pylab.grid(b=True, which='major', color='b', linestyle='-')
    pylab.rcParams['legend.loc'] = 'best'
    pylab.legend()
    pylab.show()
