#!/usr/bin/env python
import sys
import numpy
import datetime
from datetime import date

def convdata(s):
    ano,mes,dia=(s[:4],s[4:6],s[6:])
    return datetime.date(int(ano),int(mes),int(dia))

def convquote(s):
    return int(s)/100.0

def convstrip(s):
    return s.rstrip()

#nome,len,dtype,convertfunction
format=[('tipo',2,(str,8),convstrip),
        ('date',8,date,convdata),
        ('bdi',2,(str,8),convstrip),
        ('papel',12,(str,8),convstrip),
        ('merc',3,(str,8),convstrip), #010=acao, 070=call, 080=put
        ('nomeres',12,(str,8),convstrip),
        ('especi',10,(str,8),convstrip),
        ('prazo',3,(str,8),convstrip),
        ('moeda',4,(str,8),convstrip),
        ('open',13,float,convquote),
        ('high',13,float,convquote),
        ('low',13,float,convquote),
        ('med',13,float,convquote),
        ('close',13,float,convquote),
        ('compr',13,float,convquote),
        ('venda',13,float,convquote),
        ('negocios',5,(str,8),convstrip),
        ('quantidade',18,(str,8),convstrip),
        ('volume',18,(str,8),convstrip),
        ('exercicio',13,float,convquote),
        ('indopc',1,(str,8),convstrip),
        ('vencimento',8,date,convdata),
        ('fatcot',7,(str,8),convstrip),
        ('ptoexe',13,float,convquote),
        ('codisi',12,(str,8),convstrip),
        ('dismes',3,(str,8),convstrip),
]

dtypes=[(x[0],x[2]) for x in format]

def cut(v,s,convfunction):
    return convfunction(v[:s]),v[s:]

def readfile(f):
    if type(f)==str:
        with open(f) as f2:
            return readfile(f2)
    result=[]
    for line in f:
        tipo=line[:2]
        if tipo=='01':
            data=[]
            for x in format:
                val,line=cut(line,x[1],x[3])
                data.append(val)
            result.append(tuple(data))
    result=numpy.array(result,dtype=dtypes)
    return result.view(numpy.recarray)
