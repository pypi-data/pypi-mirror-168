import types
import sys, os
import ast
import types
import time
import builtins
import re

# class FileIOWrapper(_io.FileIO):
#     def __init__(self, buffer):
#         super().__init__(buffer)
    
#     def __lshift__(self, data):
#         print(type(data))
#         self.write(data)

#     def __rshift__(self, pointer):
#         pointer = self.read()

# def open(path,mode="r",buffering=-1,encoding=None,errors=None,newline=None,closefd=True,opener=None):
#     return FileIOWrapper(builtins.open(path,mode,buffering,encoding,errors,newline,closefd,opener))

def get_key_value(item, sep="="):

    key, _, value = item.partition(sep)
    return key, value


def get_log_level(level):
    
    import logging

    levels =  {
        "FATAL"     : logging.FATAL,
        "ERROR"     : logging.ERROR,
        "WARNING"   : logging.WARNING,
        "WARN"      : logging.WARN,
        "INFO"      : logging.INFO,
        "DEBUG"     : logging.DEBUG,
        "NOTSET"    : logging.NOTSET }
    
    return levels.get(level, logging.NOTSET)


def get_log_file(file=None):

    path = "./"
    if is_linux() or is_mac():
        path = "/var/log"
    
    if file:
        return os.path.join(path, file)
    return path


def get_err(exception):
    if exception.args:
        return str(exception.args[0]) + "\n"
    return exception.__class__.__name__ + "\n"
    

def ssh_key(key):
    path = os.path.join("~",".ssh", key)
    return os.path.expanduser(path)


def is_mac():
    return sys.platform == 'darwin'


def is_windows():
    return not sys.platform == 'darwin' and 'win' in sys.platform
    

def is_linux():
    return sys.platform.startswith('linux')


def set_at(data, value, id, default):

    while len(data) < id:
        data.append(default)
    if id == len(data):
        data.append(value)
    else:
        data[id] = value


def get_at(data, id):

    if id < len(data):
        return data[id]


def to_bool(value):

    if value in ("True", "true", "1"):
        return True
    if value in ("False", "false", "0"):
        return False


def wait_forever(sleeptime=1):

    while True:
        time.sleep(sleeptime)


def get_stdin(msg=""):

    if sys.stdin.isatty():
        return input(msg)
    return "/n".join(sys.stdin)


def token(value):

    try:
        return ast.literal_eval(value)
    except:
        return value


def is_shared_library(file):

    *_, ext = os.path.splitext(file)
    
    if is_linux():
        return ext == ".so"
    if is_windows():
        return ext in (".dll", ".pyd")
    if is_mac():
        return ext in (".so", ".dylib")

def is_python(path):

    if os.path.isfile(path):
        *_, ext = os.path.splitext(path)
        return ext == ".py"
    return is_module(path)


def is_module(path):

    if os.path.isdir(path):
        return "__init__.py" in os.listdir(path)
    return False


def get_key_by_value(dic, value, default=None):

    for k,v in dic.items():
        if v == value:
            return k
    return default


def contains(value, items):
    for i in items:
        if i in value:
            return True
    return False


def load_module(module_name):

    if os.path.exists(module_name):
        sys.path.append(os.path.dirname(module_name))
        module_name = os.path.basename(module_name)
        
    try:
        module = __import__(module_name, globals(), locals())
    except Exception as ex:
        print("Could not load module {module_name} :", ex)
        module = module_name
        
    return module


def to_list(value):
        if not type(value) == list:
            return [value]
        return value


def enum_variables(text, start="{", end="}"):
    regex = r"\%s(.*?)\%s"%(start, end)
    matches = re.findall(regex, text)
    for match in matches:
        yield match


def setmembers(**kwargs):
    def factory(func):
        for k,v in kwargs.items():
            setattr(func, k, v)
        return func
    return factory


def setmethods(**kwargs):
    def factory(func):
        for k,v in kwargs.items():
            setattr(func, k, types.MethodType(v, func))
        return func
    return factory


def fix_debugger_args():
    if len(sys.argv) > 2:
        if sys.argv[0] == "env" and sys.argv[1] == "PTVSD_LAUNCHER_PORT":
            sys.argv = ["python3"].extend(sys.argv[5:])


class PropertySetter(object):
    def __init__(self, func, doc=None):
        self.func = func
    def __set__(self, obj, value):
        return self.func(obj, value)


