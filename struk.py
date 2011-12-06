'''Utils for using string as unique key'''
import math

CHARS_ALLOWED = '0123456789' +\
                'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +\
                'abcdefghijklmnopqrstuvwxyz'
BASE = len(CHARS_ALLOWED)

def int2str(id):
    '''generate string from id'''
    str = ''
    i = 1
    while True:
        cur_base = int(math.pow(BASE, i))
        remainder = id % cur_base
        digit = int(remainder / math.pow(BASE, i-1))
        str = CHARS_ALLOWED[digit] + str
        
        id -= remainder
        i += 1
        
        if id <= 0:
            break
    
    return str 

def str2int(str):
    '''calculate int from str'''
    i = len(str) - 1
    id = 0
    
    for c in str:
        id += CHARS_ALLOWED.index(c) * int(math.pow(BASE, i))
        i -= 1
        
    return id

def increase(str, step=1):
    '''Increase strpk by step (default 1)'''
    return int2str(str2int(str)+step)