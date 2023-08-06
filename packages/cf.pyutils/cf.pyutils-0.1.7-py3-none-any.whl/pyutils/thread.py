from threading import Thread, RLock, Event
from .decorators import loop

def thread(name=""):
    def factory(func):
        def wrapper(*args, **kwargs):
            th = Thread(target=func, name=name, args=args, kwargs=kwargs)
            th.start()
            return th
        return wrapper
    if callable(name):
        func=name
        name=func.__name__
        return factory(func)
    return factory

def register_async(*args, **kwargs):
    import asyncore
    def factory(cls):
        cls(*args, **kwargs)
        try: asyncore.loop()
        except KeyboardInterrupt: pass
    return factory

def delay(event, timeout=1):
    def factory(func):
        def wrapper(*args, **kwargs):
            while True:
                flag = event.wait(timeout)
                event.clear()
                if flag is True:
                    continue
                return func(*args, **kwargs)
        return wrapper
    return factory

def lock(item):
    def factory(func):
        def wrapper(*args, **kwargs):
            with item:
                return func(*args, **kwargs)
        return wrapper
    if not hasattr(lock, "_IDs"):
        setattr(lock, "_IDs", dict())
    if not type(item) == RLock:
        item = getattr(lock, "_IDs").setdefault(item, RLock())
    return factory

def loop_thread(arg=None, looptime=None, name=""):
    event=arg
    flag=False

    def factory(func):
        func=loop(looptime)(func)
        def wrapper(*args, **kwargs):
            def looper(*args, **kwargs):
                while not event.is_set():
                    func(*args, **kwargs)
                event.clear()
            th = thread(name)(looper)(*args, **kwargs)
            if flag: return th, event
            return th
        return wrapper
    
    if not isinstance(arg, Event):
        event=Event()
        flag=True
    if callable(arg):
        return factory(arg)
    return factory

class ThreadPool:

    def __init__(self, max_thread=None):
        self.max_thread = max_thread
        self.__num_thread = 0
        self.__pool = list()
        self.__lock = RLock()

    def join(self, thread):
        with self.__lock:
            self.__pool.append(thread)
            self.__num_thread += 1

    def wait_all(self):
        with self.__lock:
            while self.__num_thread:
                for th in self.__pool:
                    th.join()
                    self.__num_thread -= 1
