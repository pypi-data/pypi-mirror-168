import os
from .config import ConfigError
import inspect

def qevent_filter(event_type):
    def factory(func):
        def wrapper(self, event):
            if event.type() == event_type:
                func(self, event)
            return super(self.__class__.__bases__[0], self).event(event)
        return wrapper
    return factory

def stylize(config=None, name=None):

    def _wrapper(cls):
        init=cls.__init__
        def wrapper(*args, **kwargs):
            filename=name
            if not name: filename=f"{cls.__name__}.css"
            path = _get_style_file(filename)
            super(cls, args[0]).__init__()
            if not path == None:
                with open(path) as file:
                    args[0].setStyleSheet(file.read())
            return init(*args, **kwargs)
        return wrapper
    
    def _get_style_file(fname):
        if not config == None:
            try: return getattr(config.styles, fname)
            except (AttributeError, ConfigError):
                try:
                    folder=config.path.style
                    fullpath=os.path.join(folder, fname)
                    if os.path.isfile(fullpath):
                        return fullpath
                except (AttributeError, ConfigError): pass
        if os.path.isfile(fname):
            return fname
        print(f"style sheet for class {fname} not found")
                    
    def factory(cls):
        cls.__init__ = _wrapper(cls)
        return cls

    if inspect.isclass(config):
        config.__init__ = _wrapper(config)
        return config
    return factory