#!/usr/bin/python
import bmfutils
import datetime
import pylab
import numpy

#quotes=bmfutils.readfile('COTAHIST_A2014.TXT')
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

papeis=['PETR%s%s'%(y,x) for y in ['A','B','C','D','E'] for x in [12,13,14,15,16,18,19]]
alt=0.3
def plot2():
    ndays2=60
    for alter1,alter2 in [(-1.4,0),(0,0),(1.4,0)]:
        for ndays in [60]:
            qp=quotes[[i for i,x in enumerate(quotes.papel) if x in papeis]]
            #qp=qp[qp.date>=dti]
            #qp=qp[qp.date<dtf]
            daystoexp=numpy.array([x.days for x in qp.vencimento-qp.date])
            mask=daystoexp<ndays
            qp=qp[mask]
            daystoexp=numpy.array([x.days for x in qp.vencimento-qp.date])
            mask=daystoexp>ndays-ndays2
            qp=qp[mask]
            daystoexp=numpy.array([x.days for x in qp.vencimento-qp.date])
            precoacao=numpy.array([petr4[petr4.date==xdate]['close'][0] for xdate in qp.date])
            dist=precoacao-qp.exercicio
            ivalue=[x>0 and x or 0 for x in dist]
            tvalue=qp.close-ivalue
            predict=predictcalltvalue(precoacao,qp.exercicio,daystoexp,alter1,alter2)
            diff=predict-tvalue
            #pylab.plot(dist,tvalue,'+',label='tvalue %s'%dti)
            #pylab.plot(dist,predict,'x',label='predict %s'%dti)
            pylab.plot(dist,diff,'x',label='%s:%s'%(ndays,alter1))
    
def callivalue(precoacao,precoexercicio):
    dist=precoacao-precoexercicio
    absdist=numpy.abs(dist)
    return (dist+absdist)/2

def predictcalltvalue(precoacao,precoexercicio,daystoexp,alter1=0.0,alter2=0.0):
    dist=precoacao-precoexercicio
    absdist=numpy.abs(dist)
    factor1=(1.0)*daystoexp/100.0+0.3
    factor2=(0.0)*daystoexp/100.0+2.0+alter1
    predict=-0.05+factor1*numpy.exp((-1)*absdist/factor2)
    return predict

def predictcallfvalue(precoacao,precoexercicio,daystoexp):
    return predictcalltvalue(precoacao,precoexercicio,daystoexp)+callivalue(precoacao,precoexercicio)
    
def plot3():
    for dist in [-2.0,-1.0,0.0,1.1,2.1]:
        days = numpy.arange(120,0,-1)
        precoacao=numpy.array([15.0,]*len(days))
        precoexercicio=numpy.array([15.0+dist,]*len(days))
        predict=predictcalltvalue(precoacao,precoexercicio,days)
        pylab.plot(days,predict,'.',label='%s'%(dist))

def plotcall(exercicio,daystoexp,max=30):
    price=numpy.arange(0,max,0.005)
    predict=predictcallfvalue(price,exercicio,daystoexp)
    pylab.plot(price,predict,'-',label='%s:%s'%(exercicio,daystoexp))

def plotratio(exercicio1,exercicio2,daystoexp,max=30):
    price=numpy.arange(0,max,0.005)
    predict=-predictcallfvalue(price,exercicio1,daystoexp)+2*predictcallfvalue(price,exercicio2,daystoexp)
    pylab.plot(price,predict,'-',label='%s:%s:%s'%(exercicio1,exercicio2,daystoexp))

def ploticall(exercicio,max=30):
    price=numpy.arange(0,max,0.005)
    predict=callivalue(price,exercicio)
    pylab.plot(price,predict,'-',label='%s:0'%(exercicio))
        

v1=14
v2=15
plotcall(16,30,max=20)
ploticall(v1,max=20)
ploticall(v2,max=20)
ploticall(16,max=20)
plotratio(v1,v2,60,max=20)
plotratio(v1,v2,30,max=20)
plotratio(v1,v2,0,max=20)


ax = pylab.plt.gca()
#ax.set_yscale('log')
pylab.grid(b=True, which='major', color='b', linestyle='-')
pylab.rcParams['legend.loc'] = 'best'
pylab.legend()
pylab.show()
