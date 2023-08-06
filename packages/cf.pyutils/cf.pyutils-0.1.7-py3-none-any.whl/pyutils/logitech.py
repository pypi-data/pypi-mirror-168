from .math import clamp

def register_led_function(id=None):
    def factory(func):
        func._id = func.__name__ if id == None else id
        return func
    return factory

def rgb_to_logi(r,g,b):
    return (int(clamp(r*100,maxValue=100)),
            int(clamp(g*100,maxValue=100)),
            int(clamp(b*100,maxValue=100)))

def logi_norm(func):
    def wrapper(*args, **kwargs):
        return rgb_to_logi(*func(*args, **kwargs))
    return wrapper