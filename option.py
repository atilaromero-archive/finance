#!/usr/bin/python
import datetime
import pylab
import numpy as np

class Option:
    def __add__(self,y):
        ret=Option()
        ret.tvalue=self.tvalue+y.tvalue
        ret.ivalue=self.ivalue+y.ivalue
        ret.value= self.value+y.value
        assert np.all(self.prices==y.prices)
        ret.prices=self.prices
        return ret
    
    def __sub__(self,y):
        ret=Option()
        ret.tvalue=self.tvalue-y.tvalue
        ret.ivalue=self.ivalue-y.ivalue
        ret.value= self.value-y.value
        assert np.all(self.prices==y.prices)
        ret.prices=self.prices
        return ret

    def plot(self,*args,**kwargs):
        pylab.plot(self.prices,self.value,*args,**kwargs)   
    
class Call(Option):
    #      [ , x, ln(d), xln(d)]
    params=[-2.538, -1.9264, 0.60037, 0.3063]
    #params=[0.9083, -1.3003500000000001, -0.36683, 0.47369]
    #params=[1.1303, -1.41145, -0.36673, 0.47369]
    def __init__(self,precoexercicio,precoacao,daystoexp):
        dist=precoacao-precoexercicio
        absdist=np.abs(dist)
        p=Call.params
        x=absdist
        lnd=np.log(daystoexp)
        self.prices=precoacao
        self.tvalue=np.exp(p[0] + p[1]*x + p[2]*lnd + p[3]*x*lnd)
        self.ivalue=(dist+absdist)/2.0
        self.value=self.tvalue+self.ivalue

class Put(Option):
    # [ , x, ln(d), xln(d)]
    params=[-2.41259, -1.86588, 0.50489, 0.27775]
    def __init__(self,precoexercicio,precoacao,daystoexp):
        dist=precoexercicio-precoacao
        absdist=np.abs(dist)
        p=Put.params
        x=absdist
        lnd=np.log(daystoexp)
        self.prices=precoacao
        self.tvalue=np.exp(p[0] + p[1]*x + p[2]*lnd + p[3]*x*lnd)
        self.ivalue=(dist+absdist)/2.0
        self.value=self.tvalue+self.ivalue

def plotspread(exercicio1,exercicio2,daystoexp,min=12,max=20):
    price=np.arange(min,max,0.005)
    option1=Call(exercicio1,price,daystoexp)
    option2=Call(exercicio2,price,daystoexp)
    opt=option1-option2
    pylab.plot(price,opt.value,'-',label='%s:%s:%s'%(exercicio1,exercicio2,daystoexp))

if __name__=="__main__":
    price=np.arange(12,20,0.005)
    ex=16
    d=30
    a=Put(ex,price,d)
    b=Call(ex,price,d)
    c=a+b
    a.plot('-',label='%s:%s'%(ex,d))
    b.plot('-',label='%s:%s'%(ex,d))
    c.plot('-',label='%s:%s'%(ex,d))
    (Put(15.5,price,d)+Call(16.5,price,d)).plot('-',label='%s:%s'%(ex,d))
    (Put(15,price,d)+Call(17,price,d)).plot('-',label='%s:%s'%(ex,d))
    (Put(14,price,d)+Call(18,price,d)).plot('-',label='%s:%s'%(ex,d))

    ax = pylab.plt.gca()
    #ax.set_xscale('log')
    #ax.set_yscale('log')
    pylab.grid(b=True, which='major', color='b', linestyle='-')
    pylab.rcParams['legend.loc'] = 'best'
    pylab.legend()
    pylab.show()
