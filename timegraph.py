#!/usr/bin/python
import bmfutils
import datetime
import pylab
import numpy as np

#quotes=bmfutils.readfile('COTAHIST_A2013.TXT')
quotes=bmfutils.readfile('test.data')
papeis=['PETRE14' ,
        'PETRE15' ,
        'PETRE16' ,
        'PETRE18' ,
        'PETRQ14' ,
        'PETRQ15' ,
        'PETRQ16' ,
        'PETRQ18' ,
        'PETRR15' ,
        'PETRR16' ,
        'PETRD14' ,
        'PETRD16' ,
        'PETRD17' ,
]

petr4=quotes[quotes.papel=='PETR4']

def plot1():
    for p in papeis[:4]:
        qp=quotes[quotes.papel==p]
        daystoexp=[x.days for x in qp.vencimento-qp.date]
        _petr=petr4[[i for i,d in enumerate(petr4.date) if d in qp.date]]
        dist=_petr.close-qp.exercicio
        absdist=[abs(x) for x in dist]
        ivalue=[x>0 and x or 0 for x in dist]
        tvalue=qp.close-ivalue
        #pylab.plot_date(qp.date,qp.close,'.',label='close %s'%p)
        #pylab.plot_date(qp.date,ivalue,'.',label='ivalue %s'%p)
        pylab.plot(dist,tvalue,'.',label='tvalue %s'%p)

def callivalue(precoacao,precoexercicio):
    dist=precoacao-precoexercicio
    absdist=np.abs(dist)
    return (dist+absdist)/2

def predictcallfvalue(precoacao,precoexercicio,daystoexp):
    return predictcalltvalue(precoacao,precoexercicio,daystoexp)+callivalue(precoacao,precoexercicio)
    
def plot3():
    for dist in [-2.0,-1.0,0.0,1.1,2.1]:
        days = np.arange(120,0,-1)
        precoacao=np.array([15.0,]*len(days))
        precoexercicio=np.array([15.0+dist,]*len(days))
        predict=predictcalltvalue(precoacao,precoexercicio,days)
        pylab.plot(days,predict,'.',label='%s'%(dist))

def plotcall(exercicio,daystoexp,max=30):
    price=np.arange(0,max,0.005)
    predict=predictcallfvalue(price,exercicio,daystoexp)
    pylab.plot(price,predict,'-',label='%s:%s'%(exercicio,daystoexp))

def plotratio(exercicio1,exercicio2,daystoexp,max=30):
    price=np.arange(0,max,0.005)
    predict=-predictcallfvalue(price,exercicio1,daystoexp)+3*predictcallfvalue(price,exercicio2,daystoexp)
    pylab.plot(price,predict,'-',label='%s:%s:%s'%(exercicio1,exercicio2,daystoexp))

def ploticall(exercicio,max=30):
    price=np.arange(0,max,0.005)
    predict=callivalue(price,exercicio)
    pylab.plot(price,predict,'-',label='%s:0'%(exercicio))
        
def testratio():
    v1=12
    v2=14
    plotcall(v1,30,max=20)
    ploticall(v1,max=20)
    ploticall(v2,max=20)
    plotratio(v1,v2,90,max=20)
    plotratio(v1,v2,45,max=20)
    plotratio(v1,v2,0,max=20)

papeis=['PETR%s%s'%(y,x) for y in ['A','B','C','D','E'] for x in [12,13,14,15,16,18,19]]
alt=0.5
def filterndays(qp,ndaysmin,ndaysmax):
    daystoexp=np.array([x.days for x in qp.vencimento-qp.date])
    mask=daystoexp<ndaysmax
    qp=qp[mask]
    daystoexp=np.array([x.days for x in qp.vencimento-qp.date])
    mask=daystoexp>=ndaysmin
    qp=qp[mask]
    return qp

def filterdist(qp,med,var):
    precoacao=np.array([petr4[petr4.date==xdate]['close'][0] for xdate in qp.date])
    dist=precoacao-qp.exercicio
    qp=qp[np.abs(dist-med)<var]
    return qp

def filterdistneg(qp):
    precoacao=np.array([petr4[petr4.date==xdate]['close'][0] for xdate in qp.date])
    dist=precoacao-qp.exercicio
    qp=qp[dist<=0]
    return qp

def linab(x1,y1,x2,y2):
    a=(y1-y2)/(x1-x2)
    b=y1-a*x1
    return a,b

def plot2():
    #ndays=[0,5,10,15,30,60,90,120]
    ndays=[0,30,90,300]
    #ndays=[0,300]
    #for alter1,alter2 in [(-alt,0),(0,0),(alt,0)]:
    for alter1,alter2 in [(0,0)]:
        for nmin,nmax in zip(ndays[:-1],ndays[1:]):
            for distmed in np.arange(-6,0.1,6):
                qp=quotes[[i for i,x in enumerate(quotes.papel) if x in papeis]]
                qp=filterndays(qp,nmin,nmax)
                #qp=filterdistneg(qp)
                qp=filterdist(qp,distmed,6)
                ### end of masks
                daystoexp=np.array([x.days for x in qp.vencimento-qp.date])
                precoacao=np.array([petr4[petr4.date==xdate]['close'][0] for xdate in qp.date])
                dist=precoacao-qp.exercicio
                ivalue=[x>0 and x or 0 for x in dist]
                tvalue=qp.close-ivalue
                predict=predictcalltvalue(precoacao,qp.exercicio,daystoexp,alter1,alter2)
                diff=predict-tvalue
                factor1=daystoexp**0.64/np.exp(2.8)
                factor2=0.65*daystoexp/100.0
                pylab.plot(dist,tvalue,'+',label='%s'%nmax)
                pylab.plot(dist,predict,'x',label='%s'%nmax)
                #pylab.plot(dist,diff,'x',label='%s'%nmax)
                #pylab.plot(daystoexp,tvalue,'x',label='%s:%s'%(nmax,distmed))
                #pylab.plot(daystoexp,predict,'x',label='%s:%s'%(nmax,distmed))
                #pylab.plot(np.log(daystoexp),np.log(tvalue),'x',label='%s:%s'%(nmax,distmed))
                #pylab.plot(np.log(daystoexp),np.log(predict),'x',label='%s:%s'%(nmax,distmed))

def predictcalltvalue(precoacao,precoexercicio,daystoexp,alter1=0.0,alter2=0.0):
    dist=precoacao-precoexercicio
    absdist=np.abs(dist)
    b=-2.54-(absdist)*2.14
    a=(b-0.885)/(-5.9)
    #factor1=(2.4)*daystoexp/100.0
    #factor1=daystoexp**0.64/np.exp(2.8)
    #factor2=0.27*daystoexp/100.0
    #predict=factor1*np.exp((-1.0)*factor2*np.abs(dist))
    predict=np.exp(b)*(daystoexp**a)
    return predict

 
x=np.arange(3,6,0.1)
d=120
factor1=d**0.64/np.exp(2.8)
factor2=1.5*d/100.0
#pylab.plot(x,factor1*np.exp((-1.0)*factor2*np.abs(x)),'.',label='plot %s'%d)
#pylab.plot(x,0.64*x-2.8,'.',label='plot %s'%d)
#pylab .plot(x,x**0.64/np.exp(2.8),'.',label='plot %s'%d)
def pf(x1,y1,x2,y2,xa=[],xb=[]):
    a,b=linab(x1,y1,x2,y2)
    xa+=[a]
    xb+=[b]
    print a,b
    pylab.plot(x,a*x+b,'-',label='plot %s'%d)
    return xa,xb

def f1():
    x1,y1=(5.9,0.885)
    pf(x1,y1,3,-1.7)
    pf(x1,y1,3,-0.8)
    pf(x1,y1,2.65,-3.2)
    pf(x1,y1,3.5,-3.2)
    xa,xb=pf(x1,y1,3.2,-4.6)
    pylab.plot(xa,xb,'*-')
    print linab(xa[0],xb[0],xa[1],xb[1])

def f2():
  for dist in np.arange(-6,0.1,1):
    days=np.arange(1,300,1)
    tval=predictcalltvalue(10-dist,10,days)
    pylab.plot(np.log(days),np.log(tval),'.')

#plot2()
plotcall(18,1)


ax = pylab.plt.gca()
#ax.set_xscale('log')
#ax.set_yscale('log')
pylab.grid(b=True, which='major', color='b', linestyle='-')
pylab.rcParams['legend.loc'] = 'best'
#pylab.legend()
pylab.show()
