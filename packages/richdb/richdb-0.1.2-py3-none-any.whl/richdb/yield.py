#!-*- encoding=utf8 -*-
def foo(n):
    print('starting')
    i = -1
    while i < n:
        i = i + 1 
        yield i

def fab(max):
    n,a,b = 0,0,1
    while b < max:
        yield b
        a,b = b, a+b
        n = n + 1

#for i in foo(100):
#    print( i )

for i in fab(100):
    print( i )