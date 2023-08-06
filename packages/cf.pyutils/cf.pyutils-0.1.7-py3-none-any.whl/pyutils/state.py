class StateType:
    RELEASED        = 1
    JUST_ACTIVE     = 1<<1
    ACTIVE          = 1<<2
    JUST_RELEASE    = 1<<3
    
    states=((RELEASED,JUST_ACTIVE),(JUST_RELEASE,ACTIVE))

# class State:
    
#     def __init__(self, condition=None):
#         self.value = StateType.RELEASED
#         self.prev = False

#     def update_state(self, new=None):
#         if self.prev > new:
#             self.value = StateType.JUST_RELEASE
#         else: self.value = 0x1<<(self.prev + new)
#         self.prev = new
#         return self.value

class State:
    def __init__(self, condition=None):
        self.value = StateType.RELEASED
        self.prev = False
    def update_state(self, new):
        self.value=StateType.states[self.prev][new]
        self.prev=new
        return self.value

def trigger_on(filter, type=StateType.JUST_ACTIVE):
    def factory(func):
        setattr(func, "_state", State())
        def wrapper(*args, **kwargs):
            state=filter(*args, **kwargs)
            if func._state.update_state(state) & type:
                return func(*args, **kwargs)
        return wrapper
    return factory