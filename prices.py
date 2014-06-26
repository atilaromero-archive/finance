#!/usr/bin/env python
import option
import blackscholes as bs
import datetime
import numpy as np

minv=15.0
maxv=17.3
vl=0.018
vh=0.020
mes=7
mytype='p'

strikes={
    8.16: 50 ,
    8.36: 52 ,
    8.56: 94 ,
    8.76: 96 ,
    8.96: 98 ,
    9.16: 10 ,
    9.41: 80 ,
    9.66: 40 ,
    10.16: 11 ,
    10.66: 41 ,
    11.16: 12 ,
    11.66: 42 ,
    12.16: 13 ,
    12.66: 43 ,
    12.91: 83 ,
    13.16: 14 ,
    13.66: 44 ,
    14.16: 15 ,
    14.66: 45 ,
    15.16: 16 ,
    15.66: 46 ,
    16.16: 7 ,
    16.66: 47 ,
    17.16: 18 ,
    17.66: 48 ,
    17.91: 82 ,
    18.16: 9 ,
    18.66: 49 ,
    19.16: 20 ,
    19.41: 81 ,
    19.66: 89 ,
    20.16: 21 ,
    20.66: 90 ,
    21.16: 92 ,
    21.66: 91 ,
    22.16: 93 ,
    22.66: 72 ,
    23.16: 24 ,
    23.66: 73 ,
    24.16: 54 ,
    25.16: 26 ,
    26.16: 56 ,
    28.16: 28 ,
    30.16: 31 ,
    32.91: 33 ,
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

if __name__=="__main__":
    r=option.Option.rate
    venc=sorted(vencimentos.keys())[mes-1]
    Xs=[x for x in sorted(strikes.keys()) if minv<=x and x<=maxv]
    print str(venc)+'\t'+'\t'.join([str(strikes[x]) for x in Xs])
    print '%1.3f-%1.3f'%(vl,vh)+'\t'+'\t'.join([str(x) for x in Xs])
    for S in np.arange(maxv,minv-0.001,-0.05):
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
