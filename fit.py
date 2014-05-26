#!/usr/bin/env python
import numpy as np

def _grade(function,params,x,y):
    nx=np.array(x)
    ny=np.array(y)
    nres=function(nx,params)
    ndist=np.abs(nres-ny)
    return np.sum(np.exp(-ndist))
    
def _try(function,params,x,y,s):
    grades=[0]*len(params)
    p=[0]*len(params)
    for i in range(len(params)):
        p[i]=params[:]
        p[i][i]=p[i][i]+s
        grades[i]=_grade(function,p[i],x,y)
    maxg=max(grades)

    return maxg,p[grades.index(maxg)]


def fit(function,parameters,x,y,step=0.1):
    """y=function(x,params)
    """
    params=parameters[:]
    present=(_grade(function,params,x,y),params)
    while True:
        params=present[1]
        tries=[0]*3
        tries[0]=_try(function,params,x,y,-step)
        tries[1]=present
        tries[2]=_try(function,params,x,y,step)
        maxg=max([a[0] for a in tries])
        if maxg==present[0]:
            return present[1]
        elif maxg==tries[0][0]:
            present=tries[0]
        else:
            present=tries[2]

def _test():
    def f(x,p):
        return x*p
    x=[1,2,3]
    y=[10,20,30]
    print 'result:',fit(f,[0,],x,y,0.01)
