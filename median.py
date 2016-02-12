#!/usr/bin/env python

def median(intList):
    intList.sort()
    if len(intList) % 2 == 0:
        numOne = len(intList) / 2
        numTwo = numOne - 1
        return (intList[numOne] + intList[numTwo]) / 2.0
    else:
        index = len(intList) / 2 + 1
        return intList[index-1]
        
print median([4,4,5,5])
