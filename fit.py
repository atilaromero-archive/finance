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
    
_grade=_grade5

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
    for i in range(100):
        tp=list(params)[:]
        tp+=((np.random.random(len(tp))-0.5)*s)
        try:
            grades.append([_grade(function,tp,x,y),tp.copy()])
        except:
            pass
    maxg=max(grades,key=(lambda x : x[0]))
    #print 'maxg',maxg
    assert _grade(function,maxg[1],x,y)==maxg[0]
    return maxg

_try=_try2

verbose=False
def fit(function,parameters,x,y,minstep=0.001):
    """y=function(x,params)
    """
    params=list(parameters)[:]
    present=(_grade(function,params,x,y),params)
    step=1
    while True:
        if verbose:
            print step,present[0]
        params=list(present[1])[:]
        new=(_try2(function,params,x,y,step))
        if new[0]>present[0]:
            step*=10.0
        else:
            if step<minstep:
                return present[1]
            step/=10.0
        present=new

def _test():
    def f(x,p):
        return x*p
    x=[1,2,3]
    y=[10,20,30]
    print 'result:',fit(f,[0,],x,y,0.01)
if __name__=='__main__':
    _test()
