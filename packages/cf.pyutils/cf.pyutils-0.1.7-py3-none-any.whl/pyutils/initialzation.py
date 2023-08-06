import sys
import inspect
from .common import token, to_list

def parse_args(args=sys.argv):

    def is_flag(key):
        length = len(key)
        if length > 1:
            num = 0
            while key[num] == "-":
                num += 1
            if num < length: return num
        return 0

    key, value = "", list()
    out = dict()

    def store(dic, key, value):
        if key:
            if not value: value = True
            elif len(value) == 1: value = value[0]
        dic[key] = value
        
    for v in args:
        flag = is_flag(v)#
        if not flag:
            value.append(token(v))
        else:
            store(out, key, value)
            key, value = v[flag:], list()
        if v is args[-1]:
            store(out, key, value)

    return out

def main(*args, **kwargs):

    def append_to_dict(dic, key, value):
        try: dic[key] = to_list(dic[key]) + to_list(value)
        except KeyError: dic[key] = value
    
    def resolve_name(func, args):
        names = inspect.getargspec(func)[0]
        out = dict()
        for k, v in args.items():
            if len(k) == 1 and not k in names:
                for i in names:
                    if k == i[0]:
                        out[i] = v
                        break
            elif not k == "":
                out[k] = v
        return args[""], out

    def factory_res(cls):
        arg, kwarg = resolve_name(cls, kwargs)
        cls(*arg, **kwarg)
        return cls
    
    def factory(cls):
        cls(*args, **kwargs)
        return cls

    if "" in kwargs.keys():
        return factory_res
    if len(args):
        if callable(args[0]):
            return args[0]()
    return factory

# def parse_args(args):
#     default = []
#     params = {}
#     for i in args:
#         if i.startswith("--"):
#             value = i.split("=")
#             if len(value) == 2:
#                 params[value[0][2:]] = token(value[1])
#         elif i.startswith("-"):
#             params[i[1:]] = True
#         else:
#             default.append(token(i))
#     return params, default