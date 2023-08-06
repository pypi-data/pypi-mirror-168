from enum import Enum, unique
import psutil

# class BitField:
#     _counter=0
#     @classmethod
#     def _next(cls):
#         return 0x1 << cls._counter
#         cls._counter+=1
#     @classmethod
#     def _last(cls):
#         return (0x1 << cls._counter) - 1

class PriorityClass:
    REALTIME        = None #psutil.REALTIME_PRIORITY_CLASS
    HIGH            = None #psutil.HIGH_PRIORITY_CLASS
    ABOVENORMAL     = None #psutil.ABOVE_NORMAL_PRIORITY_CLASS
    NORMAL          = None #psutil.NORMAL_PRIORITY_CLASS
    BELOWNORMAL     = None #psutil.BELOW_NORMAL_PRIORITY_CLASS
    LOWEST          = None #psutil.IDLE_PRIORITY_CLASS

# class FileSystemEvent(BitField):
#     CREATED     = _next()
#     DELETED     = _next()
#     MODIFIED    = _next()
#     MOVED       = _next()
#     ANY         = _last()