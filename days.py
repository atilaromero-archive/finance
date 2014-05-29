#!/usr/bin/python
import bmfutils
import pylab
import numpy as np
import fit
import blackscholes as bs

quotes=bmfutils.readfile('test.data')
petr4=quotes[quotes.papel=='PETR4']
calls=quotes[quotes.merc=='070']
puts=quotes[quotes.merc=='080']


dates=sorted(set(petr4.date))
for d in dates[:10]:
    data=[]
    precoacao=petr4[petr4.date==d].med[0]
    c=calls[calls.date==d]
    for v in sorted(set(c.vencimento))[:4]:
        t=(v-d).days
        def f(strike,p):
            r=0.00018
            v=p[0]
            return bs.BlackSholes('c',precoacao,strike,t,r,v)
        cv=c[c.vencimento==v]
        params=fit.fit(f,[0.0],cv.exercicio,cv.med)
        print params,v
        data.append(params)
        #pylab.plot(cv.exercicio,f(x,params),'x')
        #pylab.plot(cv.exercicio,tvalue,'.',label=str(v))
    pylab.plot([x[0] for x in data],[x[0] for x in data],'.',label=str(d))
    print '-----'
pylab.rcParams['legend.loc'] = 'best'
pylab.legend()
pylab.show()

