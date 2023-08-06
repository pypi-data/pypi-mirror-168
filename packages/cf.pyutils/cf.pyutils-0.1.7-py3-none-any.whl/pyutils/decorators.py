import time
import inspect

def switch(cls):
    cls.__cases = dict()
    cls.__default = None
    @classmethod
    def get_callback(cls,id):
        return getattr(cls,"_cases").get(
            id, getattr(cls,"_default"))
    cls.get_callback = get_callback
    for method in cls.__dict__.values   ():
        id = getattr(method, "_id", None)
        if not id == None:
            cls.__cases[id] = method
            continue
        if hasattr(method, "_default"):
            cls.__default = method
    return cls

def case(id):
    def factory(callback):
        callback.__id = id
        return callback
    return factory

def default(callback):
    callback.__default = True
    return callback

def loop(looptime=None):
    def factory(func):
        step = looptime
        if type(looptime) not in (int, float):
            step=1/60
        args = inspect.getargspec(func)
        flag = ("deltatime" in args[0] or not args[2] == None)
        def wrapper(*args, **kwargs):
            deltatime = time.perf_counter() - wrapper.starttime
            wrapper.starttime = time.perf_counter()
            if flag: kwargs["deltatime"] = deltatime
            ret = func(*args, **kwargs)
            exectime = time.perf_counter() - wrapper.starttime
            time.sleep(max(0,step-exectime))
            return ret
        setattr(wrapper, "starttime", 0)
        return wrapper
    if callable(looptime):
        return factory(looptime)
    return factory

def feed(var):
    def factory(func):
        def wrapper(*args, **kwargs):
            var = func(*args, **kwargs)
        return wrapper
    return factory

def feed_lock(var, lock):
    def factory(func):
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            with lock:
                var = ret
        return wrapper
    return factory

def repeat(func):
    def wrapper(*args,**kwargs):
        while True:
            func(*args, **kwargs)
    return wrapper

def register(id):
    def factory(func):
        setattr(func, "_id", id)
        return func
    if callable(id):
        setattr(id, "_id", id.__name__)
        return id
    return factory

