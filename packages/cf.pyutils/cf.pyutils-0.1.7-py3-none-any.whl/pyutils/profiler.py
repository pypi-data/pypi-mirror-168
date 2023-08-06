import time

class Profiler:
    
    def __init__(self):
        self.profiles=dict()
        self.start=time.process_time()

    def __call__(self, id):
        profile = self.profiles.get(id)
        if not profile:
            profile = Profile(id)
            self.profiles[id] = profile
        return profile

    def print(self):
        total=time.process_time()-self.start
        self.start=time.process_time()
        for name, p in self.profiles.items():
            print(f"{name} : {p.total:.4f}s ({(p.total/total*100):05.2f}%)")
            p.total=0
    
class Profile:

    def __init__(self, id):
        self.id = id
        self.total=0
        self.start=0

    def __enter__(self):
        self.start=time.process_time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.total+=time.process_time()-self.start