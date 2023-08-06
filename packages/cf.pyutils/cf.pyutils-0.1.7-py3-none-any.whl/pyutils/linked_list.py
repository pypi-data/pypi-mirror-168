# class ListNode:
#     def __init__(self, value, next=None):
#         self.next = next
#         self.value = value
    
# class __BidirectionalNode(ListNode):
#     def __init__(self, value, prev, next=None):
#         prev.next = self
#         next.prev = self
#         self.prev = prev
#         super().__init__(value, next)


# class LinkedList:
#     def __new__(cls, bidirectional=False):
#         if bidirectional:
#             return __BidirectionalLinkedList.__new__()
#         return super().__new__()

#     def __init__(self):
#         self.length = 0
#         self.__start = None
#         self.__end = None

#     def __index_guard(self, func):
#         def __wrapper(*args, **kwargs):
#             if 0 <= args[1] < self.length:
#                 return func(*args, **kwargs)
#             raise IndexError
    
#     def __add(self, func):
#         def __wrapper(*args, **kwargs):
#             ret = func(*args, **kwargs)
#             self.length += 1
#             return ret
#         return __wrapper
    
#     def __sub(self, func):
#         def __wrapper(*args, **kwargs):
#             ret = func(*args, **kwargs)
#             self.length -= 1
#             return ret
#         return __wrapper

#     @__index_guard
#     def __get_item(self, index):
#         found = self.__start
#         for i in range(index):
#             found = found.next
#         return found
    
#     @__add
#     def pushback(self, value=None):
#         new = ListNode(value)
#         self.__end.next = new
#         self.__end = new

#     @__add
#     def pushfront(self, value=None):
#         self.__start = ListNode(value, self.__start)

#     @__sub
#     def popback(self, value=None):
#         del self.__end

#     @__sub
#     def popfront(self, value=None):
#         next = self.__start.next
#         del self.__start
#         self.__start = next
    
#     @__add
#     def insert(self, index, value=None):
#         found = self.__get_item(index)
#         found.next = ListNode(value, found.next)
       
#     @__sub
#     def remove(self, index):
#         found = self.__get_item(index)
#         next = found.next.next
#         del found.next
#         found.next = next

#     def __getitem__(self, index):
#         return self.__get_item(index).value

#     def __setitem__(self, index, value):
#         self.__get_item(index).value = value
    
#     def __delitem__(self, index):
#         self.remove(index)
        
# class _Linked_FIFO(FIFO):
#     pass

# class __BidirectionalLinkedList(LinkedList):
#     def __init__(self):
#         super().__init__()

#     @__index_guard
#     def __get_item(self, index):
#         if index > self.length >> 1: #optimized division by 2
#             found = self.__end
#             for i in range(index):
#                 found = found.prev
#         else:
#             found = self.__start
#             for i in range(index):
#                 found = found.next
#         return found
    
#     @__add
#     def pushback(self, value=None):
#         prev = self.__end
#         prev.next = __BidirectionalNode(value, prev)
#         self.__end = prev.next

#     @__add
#     def pushfront(self, value=None):
#         next = self.__start
#         self.__start = __BidirectionalNode(value, None, next)
#         next.prev = self.__start
    
#     @__sub
#     def popfront(self, value=None):
#         next = self.__start.next
#         del self.__start
#         self.__start = next
#         if next: next.prev = None

#     @__add
#     def insert(self, index, value=None):
#         found = self.__get_item(index)
#         found.next = __BidirectionalNode(value, found, found.next)
#         found.next.next.prev = found.next

#     @__sub
#     def remove(self, index):
#         found = self.__get_item(index)
#         next = found.next.next
#         del found.next
#         found.next = next
#         found.next.prev = found

# class _Fixed_FIFO(FIFO):
#     def _opt_push(self, func):

#         def _opt_wrapper(self, data):
#             self._buffer[self._last] = data
#             self._last = (self._last + 1) & self._index_mask
#             self._fill += 1
            
#         def _wrapper(self, data):
#             self._buffer[self._last] = data
#             self._last = (self._last + 1) % self._buffer_size
#             self._fill += 1

#         if is_powerof2(self._buffer_size):
#             return _opt_wrapper
#         return _wrapper
    
#     def _push_overflow(self, func):

#         def _wrapper(self, data):
#             if self._fill == self._buffer_size:
#                 raise OverflowError
#             else:
#                 func(self, data)

#         def _overflow_wrapper(self, data):
#             func(self, data)
#             if self._fill > self._buffer_size:
#                 self.pop()
    
#         if self._overflow:
#             return _wrapper
#         return _overflow_wrapper
    
#     def _opt_pop(self, func):

#         def _opt_wrapper(self):
#             if self._fill > 0:
#                 self._first = (self._first + 1) & self._index_mask
#                 self._fill -= 1
#                 return self._buffer[self._first]

#         def _wrapper(self):
#             if self._fill > 0:
#                 self._first = (self._first + 1) % self._buffer_size
#                 self._fill -= 1
#                 return self._buffer[self._first]

#         if is_powerof2(self._buffer_size):
#             return _opt_wrapper
#         return _wrapper


#     def __init__(self, buffersize=256, overflow=False):

#         self._first = 0
#         self._last = 0
#         self._overflow = overflow
#         self._buffer_size = buffersize
#         self._fill = 0
#         self._buffer = [None]*buffersize
#         self._index_mask = buffersize - 1

#         self.push = self._push_overflow(self._opt_push(self.push))
#         self.pop  = self._opt_push(self.pop)


#     def __lshift__(self, value):
#         self.push(value)
    
#     def __rshift__(self, value):
#         value = self.pop()

# class FIFO:

#     def __new__(cls, buffersize=None, overflow=False):
#         if 
    

    # def push(self, data):
    #     pass

    # def pop(self):
    #     pass
