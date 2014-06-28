#!/usr/bin/python
def percentvar(prices):
    return (prices[1:]-prices[:-1])/prices[1:]

def var(prices):
    return (prices[1:]-prices[:-1])

