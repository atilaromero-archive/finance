#!/usr/bin/env python
import numpy as np

def _grade1(function,params,x,y):
    nx=np.array(x)
    ny=np.array(y)
    nres=function(nx,params[:])
    ndist=np.abs(nres-ny)
    return np.sum(np.exp(-ndist))
    
def _grade5(function,params,x,y):
    nx=np.array(x)
    ny=np.array(y)
    nres=function(nx,params[:])
    ndist=np.abs(nres-ny)
    return -np.std(ndist)
    
def _grade4(function,params,x,y):
    nx=np.array(x)
    ny=np.array(y)
    nres=function(nx,params[:])
    ndist=np.abs(nres-ny)+0.001
    return np.sum(1/ndist)
    
def _grade3(function,params,x,y):
    nx=np.array(x)
    ny=np.array(y)
    nres=function(nx,params[:])
    ndist=np.abs(nres-ny)
    return -(np.max(ndist))
    
def _grade2(function,params,x,y):
    nx=np.array(x)
    ny=np.array(y)
    nres=function(nx,params[:])
    ndist=(nres-ny)**2
    return np.sum(-ndist)
    
_grade=_grade1

def _try1(function,params,x,y,s):
    grades=[0]*len(params)
    p=[0]*len(params)
    for i in range(len(params)):
        p[i]=params[:]
        p[i][i]=p[i][i]+s
        grades[i]=_grade(function,p[i],x,y)
    maxg=max(grades)
    return maxg,p[grades.index(maxg)]

def _try2(function,params,x,y,s):
    grades=[[_grade(function,params[:],x,y),params]]
    for i in range(10000):
        tp=params[:]
        tp+=((np.random.random(len(tp))-0.5)*s)
        grades.append([_grade(function,tp,x,y),tp.copy()])
    maxg=max(grades,key=(lambda x : x[0]))
    print 'maxg',maxg
    assert _grade(function,maxg[1],x,y)==maxg[0]
    return maxg

_try=_try2

def fit(function,parameters,x,y,step=0.1):
    """y=function(x,params)
    """
    params=parameters[:]
    ret= list(_try2(function,params,x,y,step)[1])
    print '-=-=-=-',_grade3(function,params,x,y)
    return ret
    present=(_grade(function,params,x,y),params)
    while True:
        tries=[present]
        params=present[1]
        tries.append(_try2(function,params,x,y,step))
        maxg=max([a[0] for a in tries])
        if maxg<=present[0]:
            return present[1]
        else:
            for j in range(len(tries)):
                if maxg==tries[j][0]:
                    present=tries[j]


def _test():
    def f(x,p):
        return x*p
    x=[1,2,3]
    y=[10,20,30]
    print 'result:',fit(f,[0,],x,y,0.01)
