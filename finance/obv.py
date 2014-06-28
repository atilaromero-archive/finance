#!/usr/bin/python
from utils import *

def obv(price,volume):
    """On Balance Volume"""
    dprice=var(price)
    idx=((dprice>0)*1+(dprice<0)*(-1))*volume[1:]
    return idx.cumsum()

def retxvol(price,volume):
    idx=percentvar(price)*volume[1:]
    return idx.cumsum()

def retxvarvol(price,volume):
    idx=percentvar(price)*var(volume)
    return idx.cumsum()
