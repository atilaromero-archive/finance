#!/usr/bin/python
import numpy as np

# Cumulative normal distribution
def CND(X):
    (a1,a2,a3,a4,a5) = (0.31938153, -0.356563782, 1.781477937, -1.821255978, 1.330274429)
    L = np.abs(X)
    K = 1.0 / (1.0 + 0.2316419 * L)
    w = 1.0 - 1.0 / np.sqrt(2*np.pi)*np.exp(-L*L/2.) * (a1*K + a2*K*K + a3*pow(K,3) +
    a4*pow(K,4) + a5*pow(K,5))
    mask=X<0
    if isinstance(w,np.ndarray):
        w[mask]*=(-1)
        w[mask]+=1.0
    else:
        if mask:
            w = 1.0 - w
    return w

# Black Sholes Function
def BlackSholes(CallPutFlag,S,X,T,r,v):
    """CallPutFlag:'c' or 'p'
S: Stock price
X: Strike price
T: Time (in years?!?)
r: risk free interest rate in T
v: volatility
"""
    d1 = (np.log(S/X)+(r+v*v/2.)*T)/(v*np.sqrt(T))
    d2 = d1-v*np.sqrt(T)
    if CallPutFlag=='c':
        return S*CND(d1)-X*np.exp(-r*T)*CND(d2)
    else:
        return X*np.exp(-r*T)*CND(-d2)-S*CND(-d1)

def _test():
    print """expect:
2.13337186193
5.84628562687
got:"""
    print BlackSholes('c',60.0,65.0,0.25,0.08,0.3)
    print BlackSholes('p',60.0,65.0,0.25,0.08,0.3)
    print BlackSholes('c',np.array([60.0]),np.array([65.0]),0.25,0.08,0.3)
    print BlackSholes('p',np.array([60.0]),np.array([65.0]),0.25,0.08,0.3)
if __name__=='__main__':
    _test()
