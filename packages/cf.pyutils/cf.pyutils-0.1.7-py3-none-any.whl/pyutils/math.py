from math import sqrt

def clamp(value, minValue=0, maxValue=1):
    return min(max(minValue, value), maxValue)

def is_powerof2(value : int) -> bool :
    return value != 0 and ((value & (value - 1)) == 0)

def length(array):
    return sqrt(sum(map(lambda x: x**2, array)))

def normalize(array):
    vec_len = length(array)
    if not vec_len:
        return array
    return map(lambda x: x/vec_len, array)

def sign(x):
    return (x>0)-(x<0)

def lerp(a, b, bias):
    return a*bias + b*(1-bias)