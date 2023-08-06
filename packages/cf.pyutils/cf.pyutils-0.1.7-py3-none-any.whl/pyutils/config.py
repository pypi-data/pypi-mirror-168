from .common import token, is_windows
import configparser as cp
import sys
import os

class ConfigError(Exception):
    pass

class ConfigSection:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __getattr__(self, name):
        raise ConfigError("config do not have property : %s"%name)


class Config:
    
    def __init__(self, path, **kwargs):
        self._file = path

        self._config = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
        self._config.read(path)
        self._config.add_section("env")
        self._config.set("env", "ROOT", os.path.dirname(path))
        
        for k,v in kwargs.items():
            self._config.set("env", k, v)

        for section in self._config.sections():
            if not section == "DEFAULT":
                setattr(self, section, ConfigSection(**self.parse(section)))

    def parse(self, section):
        result = dict()
        for k,v in self._config.items(section):
            result[k] = token(v)
        return result

    def __getattr__(self, name):
        raise ConfigError("config do not have section : %s"%name)


def config_helper(name):
    def init(path, **kwargs):
        config = Config(path, **kwargs)
        current=sys.modules[name]
        for k,v in vars(config).items():
            if isinstance(v, ConfigSection):
                setattr(current, k, v)
    return init


def get_int(value, default=0):
    if isinstance(value, int):
        return value
    elif value.isdigit():
        return int(value)
    return default


def get_bool(value, default=False):
    if value.lower() in ("1", "true"):
        return True
    elif value.lower() in ("0", "false"):
        return False
    return default


def get_list(value, default=[]):
    if value:
        if is_windows():
            return value.split(";")
        return value.split(":")
    return default