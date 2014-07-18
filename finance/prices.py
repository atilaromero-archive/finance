#!/usr/bin/env python
import sys
import option
import blackscholes as bs
import datetime
import numpy as np
import plac

strikes={
    92: 8.40 ,
    94: 8.60 ,
    96: 8.80 ,
    98: 9.00 ,
    30: 9.50 ,
    10: 10.00 ,
    60: 10.25 ,
    31: 10.50 ,
    12: 11.00 ,
    61: 11.25 ,
    5: 11.50 ,
    13: 12.00 ,
    43: 12.75 ,
    14: 13.25 ,
    34: 13.50 ,
    42: 13.75 ,
    15: 14.25 ,
    35: 14.50 ,
    45: 14.75 ,
    4: 15.50 ,
    16: 16.00 ,
    17: 16.50 ,
    47: 17.00 ,
    18: 17.50 ,
    48: 18.00 ,
    19: 18.50 ,
    99: 19.00 ,
    69: 19.25 ,
    1: 19.50 ,
    20: 20.00 ,
    21: 20.50 ,
    51: 21.00 ,
    22: 21.50 ,
    53: 21.75 ,
    52: 22.00 ,
    23: 22.50 ,
    63: 23.00 ,
    24: 23.50 ,
    55: 23.75 ,
    54: 24.00 ,
    25: 24.50 ,
    65: 25.00 ,
    2: 25.50 ,
    26: 26.00 ,
    27: 26.50 ,
    57: 27.00 ,
    6: 27.25 ,
    28: 28.00 ,
    8: 28.25 ,
    29: 29.00 ,
    9: 29.25 ,
    3: 29.50 ,
    70: 30.00 ,
    11: 30.25 ,
    71: 31.00 ,
    64: 32.75 ,
}

vencimentos={
    datetime.date(2014,1 ,20):('A','M'),
    datetime.date(2014,2 ,17):('B','N'),
    datetime.date(2014,3 ,17):('C','O'),
    datetime.date(2014,4 ,22):('D','P'),
    datetime.date(2014,5 ,19):('E','Q'),
    datetime.date(2014,6 ,16):('F','R'),
    datetime.date(2014,7 ,21):('G','S'),
    datetime.date(2014,8 ,18):('H','T'),
    datetime.date(2014,9 ,15):('I','U'),
    datetime.date(2014,10,20):('J','V'),
    datetime.date(2014,11,17):('K','W'),
    datetime.date(2014,12,15):('L','X'),
}

def main(mytype='c', mes=8, price=20.60, minv=20, maxv=23, vl=0.018, vh=0.020):
    price=float(price)
    minv=float(minv)
    maxv=float(maxv)
    vl=float(vl)
    vh=float(vh)
    mes=int(mes)
    r=option.Option.rate
    venc=sorted(vencimentos.keys())[mes-1]
    Xs=[x for x in sorted(strikes.keys()) if minv<=x and x<=maxv]
    print str(venc)+'\t'+'\t'.join([str(strikes[x]) for x in Xs])
    print '%1.3f-%1.3f'%(vl,vh)+'\t'+'\t'.join([str(x) for x in Xs])
    for S in np.arange(price+1,price-1,-0.05):
        print '%1.2f'%S,
        for X in Xs:
            T=(venc-datetime.date.today()).days
            if T>=0:
                #cl=bs.BlackScholes('c',S,X,T,r,vl)
                #ch=bs.BlackScholes('c',S,X,T,r,vh)
                #pl=bs.BlackScholes('p',S,X,T,r,vl)
                #ph=bs.BlackScholes('p',S,X,T,r,vh)
                #print '\t%02.2f-%02.2f %02.2f-%02.2f'%(cl,ch,pl,ph),
                l=bs.BlackScholes(mytype,S,X,T,r,vl)
                h=bs.BlackScholes(mytype,S,X,T,r,vh)
                print '\t%02.2f-%02.2f'%(l,h),
        print

if __name__=="__main__":
    plac.call(main,sys.argv[1:])

