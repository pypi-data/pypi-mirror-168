import _io

class Logger(_io.FileIO):

    def __init__(self, file, use_timestamp=True, use_stderr=True,
                    print_log=False):
        self.print_log = print_log
        self.use_timestamp = use_timestamp
        self.file = open(file, "a")
        self._default_stderr = sys.stderr
        self._buffer = ""
        if use_stderr:
            sys.stderr = self

    def _log(self, *messages):
        if self.use_timestamp:
            date = dt.datetime.now()
            timestamp = date.strftime(r"%d.%b %Y %H:%M:%S")
            msg = f"{timestamp} : {' '.join(messages)}"
        else:
            msg = " ".join(messages), self.file.write(msg)
        msg+="\n"
        return msg, self.file.write(msg)
    
    def __call__(self, *messages):
        msg, code = self._log(*messages)
        if self.print_log:
            sys.stdout.write(msg)
            sys.stdout.flush()
        return code
    
    def write(self, data):
        self._buffer+=data
        return True
    
    def flush(self):
        _, code = self._log(self._buffer)
        self.file.flush()
        if self.print_log:
            code = self._default_stderr.write(self._buffer) and code
            return self._default_stderr.flush() and code
        return code

    # def __del__(self, instance):
    #     self.file.close()
    #     sys.stderr = self._default_stderr

# class Debug:

#     def debug(self, func):
#         if self.debug:
#             return func
#         else:
#             return (lambda *args, **kwargs: None)

#     def __init__(self, path=None, msg=[] debug=True):

#         self.__path     = path
#         self.__debug    = debug
#         self.__msg      = msg
#         self.__functs   = {}

#         if not path == None:
#             if os.path.isfile(path):
#                 with open(path) as file
#                     self.__msg += [i.strip() for i in file.readlines()]
        
#     def get_error(self, code):
#         return self.__msg[code]

#    def __getitem__(self, id):
#        return self.__msg[id]

#    @debug
#    def log(self, id, **kwargs):
#        print(self.__msg[id].format(kwargs))

# @setsetters(_stream=out)
# @setmethods(out=_set_stream)
# @setmembers(_default=sys.stdout, time=True)
# def log(*messages):
#     timestamp = (dt.datetime.now().strftime("%d.%b %Y %H:%M:%S :") if log.time else "")
#     print(timestamp, *messages)

# @PropertySetter
# def out(self, value):
#     print("setting")
#     if not value:
#         sys.stdout = self._default
#         self.__dict__["out"] = None
#         return
#     try:
#         file = open(value, "a")
#     except: log("could not open log file :", value)
#     else:
#         # sys.stdout = file
#         self.__dict__["out"] = value

# class _log_meta(type):
#     def __init__(cls, *args, **kwargs):
#         cls_stream = None
#     @property
#     def out(cls):
#         return cls._stream
#     @out.setter
#     def out(cls, value):
#         if not value:
#             sys.stdout = cls._default
#             cls._stream = None
#             return
#         print('ok')
#         try:
#             file = open(value)
#         except:
#             cls._log("could not open log file :", value)
#         else:
#             sys.stdout = file
#             cls._stream = value

# def setters(**kwargs):
#     def factory(cls):

#         def _template(cls):
#             return getattr(cls, value)

#         for name, value in kwargs.items():

#             if type(value) == tuple and len(value) == 2:

#                 setter = getattr(cls, value[0])
#                 if setter == None : continue
#                 item, default = value[1], None

#             elif type(value) == str:

#                 setter = getattr(cls, value)
#                 if setter == None : continue
#                 tag = getattr(setter, "_set")
#                 if tag == None : continue
#                 item, default = tag

#             else: continue

#             prop = property(types.FunctionType(_template.__code__, {"value":item}, name,
#                                     _template.__defaults__, _template.__closure__))                 
#             prop.setter(setter)
#             setattr(cls.__metaclass__, item, default)
#             setattr(cls.__metaclass__, setter, prop)

#         return cls

#     return factory

# def setter(**kwargs):
#     def factory(func):
#         setattr(func, "_set", list(kwargs.items())[0])
#         return func
#     return factory


# class log(object, metaclass=setters(out="_log")):
#     time = True
#     _stream = None
#     _default = sys.stdout

#     @classmethod
#     @setter(_stream=None)
#     def _log(cls, *args):
#         timestamp = dt.datetime.now().strftime("%d.%b %Y %H:%M:%S : ") if log.time else ""
#         print(timestamp, *args)

#     def __new__(cls, *args):
#         cls._log(*args)

# def setsetters(**kwargs):

#     def _template(cls):
#         return getattr(cls, value)

#     def factory(func):
#         for k,v in kwargs.items():
#             f = types.FunctionType(_template.__code__, {"value":k}, v.__name__,
#                                     _template.__defaults__, _template.__closure__)
#             prop = property(f)                 
#             setter = prop.setter(types.MethodType(v, func))
#             setattr(func, k, None)
#             setattr(func, v.__name__, prop)
#             setattr(func, v.__name__, setter)
#         return func
    
#     return factory




