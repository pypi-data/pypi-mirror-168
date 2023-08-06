import inspect
import os

# def current_module_prefix(file):

#     module = sys.modules["__main__"]
#     return os.path.join(os.path.dirname())

def common_suffix(path1, path2):
    index = 1
    try:
        while path1[-index] == path2[-index]:
            index += 1
    except IndexError:
        pass
    return path1[len(path1)-index-1:]


def join_module_path(path):
    callstack = inspect.stack()[1]
    module = inspect.getmodule(callstack[0])
    return os.path.join(os.path.dirname(module.__file__), path)


def has_hidden(path):
    path, entity = os.path.split(path)
    if not path or (path == "/" and not entity):
        return False
    if entity.startswith(".") and not entity in ("..", "."):
        return True
    return has_hidden(path)


def remove_first(path):
    if path.count("\\") or path.count("/"):
        while path[0] not in ("\\","/"):
            path = path[1:]
        return path[1:]
    return path


def get_first(path):
    counter = 0
    if path.count("\\") or path.count("/"):
        while path[0] not in ("\\","/"):
            counter+=1
        return path[:counter]
    return path
    

def get_filename(path):
    return os.path.splitext(os.path.basename(path))[0]