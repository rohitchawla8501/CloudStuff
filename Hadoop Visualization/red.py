#! /usr/bin/python

import sys

mydict = {}

sales = 0
oKey = None

for line in sys.stdin:
    data=line.strip().split("\t")

    

	K, Sale = data

    if oKey and oKey != K:
        mydict[oldKey] = float(sales)
        salesTotal = 0

    oKey = Key
    sales += float(Sale)

if oldKey!= None:
    mydict[oKey] = float(sales)

maximum = max(mydict, key=mydict.get)
print(maximum, mydict[maximum])
