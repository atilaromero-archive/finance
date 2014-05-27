#!/usr/bin/python
import bmfutils
import datetime
import pylab
import numpy as np
import option
import fit

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

def filterndays(qp,ndaysmin,ndaysmax):
    daystoexp=np.array([x.days for x in qp.vencimento-qp.date])
    mask=daystoexp<ndaysmax
    qp=qp[mask]
    daystoexp=np.array([x.days for x in qp.vencimento-qp.date])
    mask=daystoexp>=ndaysmin
    qp=qp[mask]
    return qp

def filterdist(qp,med,var):
    precoacao=np.array([petr4[petr4.date==xdate]['high'][0] for xdate in qp.date])
    dist=precoacao-qp.exercicio
    qp=qp[np.abs(dist-med)<var]
    return qp

def filterdistneg(qp):
    precoacao=np.array([petr4[petr4.date==xdate]['high'][0] for xdate in qp.date])
    dist=precoacao-qp.exercicio
    qp=qp[dist<=0]
    return qp

def filterdistpos(qp):
    precoacao=np.array([petr4[petr4.date==xdate]['high'][0] for xdate in qp.date])
    dist=precoacao-qp.exercicio
    qp=qp[dist>=0]
    return qp

def fcall(x,params):
    option.Call.params=params
    return option.Call(x[0],x[1],x[2]).value

def fput(x,params):
    option.Put.params=params
    return option.Put(x[0],x[1],x[2]).value

def paramsCall():
    return paramsOpt(filterdistneg,option.Call.params,fcall)

def paramsPut():
    return paramsOpt(filterdistpos,option.Put.params,fput)

def paramsOpt(filtr,params,func):
    qp=quotes[[i for i,x in enumerate(quotes.papel) if x in papeis]]
    qp=filtr(qp)
    daystoexp=np.array([x.days for x in qp.vencimento-qp.date])
    precoacao=np.array([petr4[petr4.date==xdate]['high'][0] for xdate in qp.date])
    p=params
    for step in list(10.0**(-np.arange(6))):
        print 'step',step
        for asd in range(10):
            p=fit.fit(func,p,[qp.exercicio,precoacao,daystoexp],qp.high,step=step)
    return p

petr4=quotes[quotes.papel=='PETR4']
papeis=['PETR%s%s'%(y,x) for y in ['A','B','C','D','E'] for x in [12,13,14,15,16,18,19]]
#print 'Call:',paramsCall()
papeis=['PETR%s%s'%(y,x) for y in ['M','N','O','P','Q'] for x in [12,13,14,15,16,18,19]]
print 'Put:',paramsPut()
