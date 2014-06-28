#!/usr/bin/python
import pylab
import numpy
import matplotlib.mlab
from utils import *

def plotreturnshist(returns):
    n,bins,patches=pylab.hist(returns,100)
    mu=numpy.mean(returns)
    sigma = numpy.std(returns)
    x = matplotlib.mlab.normpdf(bins, mu, sigma)
    pylab.plot(bins, x, color='red')

def plotclosexvolume(sp,**kargs):
    pylab.plot(sp.close,sp.volume,".",**kargs)

def plotreturnsxvarvolume(sp,**kargs):
    pylab.plot(percentvar(sp.close),var(sp.volume),".",**kargs)

