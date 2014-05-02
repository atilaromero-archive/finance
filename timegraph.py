#!/usr/bin/python
import bmfutils
import datetime
import pylab

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
        qp=qp[qp.date>datetime.date(2014,)]
        daystoexp=[x.days for x in qp.vencimento-qp.date]
        _petr=petr4[[i for i,d in enumerate(petr4.date) if d in qp.date]]
        dist=_petr.close-qp.exercicio
        absdist=[abs(x) for x in dist]
        ivalue=[x>0 and x or 0 for x in dist]
        tvalue=qp.close-ivalue
        #pylab.plot_date(qp.date,qp.close,'.',label='close %s'%p)
        #pylab.plot_date(qp.date,ivalue,'.',label='ivalue %s'%p)
        pylab.plot(dist,tvalue,'.',label='tvalue %s'%p)

def plot2():
    for dti,dtf in [(datetime.date(2014,x,1),datetime.date(2014,x+1,1)) for x in [1,2,3,4]]:
        qp=quotes[[i for i,x in enumerate(quotes.papel) if x in papeis[:4]]]
        qp=qp[qp.date>=dti and qp.date<dtf]
        daystoexp=[x.days for x in qp.vencimento-qp.date]
        _petr=petr4[[i for i,d in enumerate(petr4.date) if d in qp.date]]
        dist=_petr.close-qp.exercicio
        absdist=[abs(x) for x in dist]
        ivalue=[x>0 and x or 0 for x in dist]
        tvalue=qp.close-ivalue
        #pylab.plot_date(qp.date,qp.close,'.',label='close %s'%p)
        #pylab.plot_date(qp.date,ivalue,'.',label='ivalue %s'%p)
        pylab.plot(dist,tvalue,'.',label='tvalue %s'%p)

plot2()

ax = pylab.plt.gca()
#ax.set_yscale('log')
pylab.grid(b=True, which='major', color='b', linestyle='-')
pylab.rcParams['legend.loc'] = 'best'
pylab.legend()
pylab.show()
