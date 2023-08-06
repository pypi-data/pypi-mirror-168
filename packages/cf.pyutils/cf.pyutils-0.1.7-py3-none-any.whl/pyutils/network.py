class RPC_Protocol:
    GET  = 0x0
    SET  = 0x1
    CALL = 0x2
    
class ProtocolStack:
    pass

# @switch
# class RPC(ProtocolStack):

#     def __init__(self, in_port=8001, out_port=8002, password=None, max_buffer=1024):

#         self.__in_port = in_port
#         self.__out_port = out_port
#         self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.__socket.setblocking(False)
#         self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)


#         self.__socket.bind(("", in_port))
#         #self.__socket.listen(1)
#         self.__max_buffer = max_buffer
#         self.__connection = None
#         self.__address = None
#         self.__lock = _thread.RLock()

#         #self.connect()

#     def connect(self):
#         def wait_connection(self):
#             conn , addr = self.__socket.accept()
#             with self.__lock:
#                 self.__connection = conn
#                 self.__address = addr
#                 self.__connection.setblocking(False)

#         _thread.start_new_thread(wait_connection, (self,))
    
#     def check_connection(fself, func):
#         def wrapper(self):
#             with self.__lock:
#                 if not self.__connection == None:
#                     return func(self)
#         return wrapper

#     #@check_connection
#     def update(self):
#         while True:
#             try:
#                 data, addr = self.__socket.recvfrom(self.__max_buffer)
#             except:
#                 break

#             # if data == b"":
#             #     self.__connection.close()
#             #     print("disconnected")
#             #     self.connect()
#             #     break

#             callback = self.__class__.__bases__[0].get_callback(data[0])
#             if not callback == None:
#                 callback(self, data[1:])


#     def send(self, data):
#         if not self.__connection == None:
#             self.__socket.sendto(data, ("localhost", self.__out_port))
#             #self.__connection.send(data)
    
#     @case(RPC_Protocol.CALL)
#     def call(self, data):
#         function_id = struct.unpack("=H",data[:2])[0]
#         callback = self.get_callback(function_id)
#         if not callback == None:
#             callback(self, data[2:])

#     @case(RPC_Protocol.GET)
#     def get(self, data):
#         format  = data[0]
#         key     = data[1:].decode("utf-8")
#         if hasattr(self, key):
#             value = self.__getattribute__(key)
#             self.__connection.send(struct.pack(format, value))
    
#     @case(RPC_Protocol.SET)
#     def set(self, data):
#         fmt_len = data[0]
#         format  = data[1:fmt_len].decode("utf-8")
#         dat_len = struct.calcsize(format)
#         d_start = fmt_len+1
#         datas   = struct.unpack(format, data[d_start:dat_len])
#         key     = data[d_start + dat_len:]
#         if hasattr(self, key):
#             if len(datas) == 1:
#                 datas = datas[0]
#             self.__setattr__(key, datas)