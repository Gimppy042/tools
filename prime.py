#!/usr/bin/env python

def is_prime(x):
    prime = False
    if x < 2:
        return prime
        
    for number in range(2, x):
        if x % number == 0:
            return prime
    else:
        print "%d is a primer number" % x
        prime = True
        return prime
