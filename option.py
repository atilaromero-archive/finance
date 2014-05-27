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
    params=[-2.7377693486652737, -1.1793911104740262, 0.63531339107274065, 0.16006923396045747]
    params=[-2.9498013116793156, -1.3902570901084326, 0.69300558122785316, 0.18147226270992628]
    def __init__(self,precoexercicio,precoacao,daystoexp):
        dist=precoacao-precoexercicio
        absdist=np.abs(dist)
        p=list(Call.params)
        x=absdist
        lnd=np.log(daystoexp)
        self.prices=precoacao
        self.tvalue=np.exp(p[0] + p[1]*x + p[2]*lnd + p[3]*x*lnd)
        self.ivalue=(dist+absdist)/2.0
        self.value=self.tvalue+self.ivalue

class Put(Option):
    # [ , x, ln(d), xln(d)]
    params=[-2.41259, -1.86588, 0.50489, 0.27775]
    params=[-2.3600902132900243, -1.8132129781771538, 0.49474942606743461, 0.2648205011754966]
    params=[-2.185689957054469, -1.4892686558017223, 0.44642311025741899, 0.19359798564991582]#close
    params=[-1.3023556772627178, -1.1653724402371433, 0.30425680666021426, 0.12490090657926957]#high
    params=[-1.0041455419858909, -2.0028617354027749, 0.21863266572499931, 0.31531627424611591]
    def __init__(self,precoexercicio,precoacao,daystoexp):
        dist=precoexercicio-precoacao
        absdist=np.abs(dist)
        p=list(Put.params)
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
    price=np.arange(16,19,0.005)
    ex=16
    d=21
    a=Put(16.66,price,d)
    b=Call(19.16,price,d)
    c=a+b
    a.plot('-')
    b.plot('-')
    c.plot('-')

    ax = pylab.plt.gca()
    #ax.set_xscale('log')
    #ax.set_yscale('log')
    pylab.grid(b=True, which='major', color='b', linestyle='-')
    pylab.rcParams['legend.loc'] = 'best'
    pylab.legend()
    pylab.show()
