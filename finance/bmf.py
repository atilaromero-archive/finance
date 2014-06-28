#!/usr/bin/env python
import sys

def cut(v,s):
    return v[:s],v[s:]

format=[('tipo',2),
        ('data',8),
        ('bdi',2),
        ('papel',12),
        ('merc',3),
        ('nomeres',12),
        ('especi',10),
        ('prazo',3),
        ('moeda',4),
        ('open',13),
        ('high',13),
        ('low',13),
        ('med',13),
        ('close',13),
        ('compr',13),
        ('venda',13),
        ('negocios',5),
        ('quantidade',18),
        ('volume',18),
        ('exercicio',13),
        ('indopc',1),
        ('vencimento',8),
        ('fatcot',7),
        ('ptoexe',13),
        ('codisi',12),
        ('dismes',3),
]
def readfile(f):
    result=[]
    for line in f:
        tipo=line[:2]
        if tipo=='01':
            data=[]
            for x in format:
                val,line=cut(line,x[1])
                data.append(val)
            result.append(data)
    return result

def campos(v,nomes):
    nomesind=[x[0] for x in format]
    indices=[nomesind.index(n) for n in nomes]
    return [[x[i] for i in indices] for x in v]

dados=readfile(sys.stdin)
nomesind=[x[0] for x in format]
for x in campos(dados,['papel','data','close','exercicio']):
    papel=x[0].strip()
    if papel==sys.argv[1]:
        ano,mes,dia=(x[1][:4],x[1][4:6],x[1][6:])
        data='%s/%s/%s'%(dia,mes,ano)
        trat=[data,
              papel,
              str(int(x[2])/100.0).replace('.',','),
              str(int(x[3])/100.0).replace('.',','),
        ]
        print '\t'.join(trat)
