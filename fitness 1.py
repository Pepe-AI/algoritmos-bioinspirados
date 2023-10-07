
import math

def fitness(decimal):
    c1=math.sin(decimal)
    c2=decimal-5
    fdex=abs(c2/c1)
    return fdex


def bi_dec(h,l):
    individuos=""
    for i in range(0,l):
        if h[i]==1:
            individuos+="1"
        else:
            individuos+="0"
    c=int(str(individuos), 2)    
    decimal_opc=c
    individuos=""
    return decimal_opc