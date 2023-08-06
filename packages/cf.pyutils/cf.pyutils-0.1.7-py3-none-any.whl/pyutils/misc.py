# Copyright 2022 matthieu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Iterator, Callable
from abc import ABCMeta, ABC, abstractmethod
from inspect import signature
from functools import partial


def override(func: Callable) -> Callable:
    func._is_overriding = True
    return func



class ClassUtils:

    def _search_for_flag(self, flag):

        yield from filter(lambda x: hasattr(x, flag), self.__dict__.values())


    def _check_overload(self) -> None:

        attribs = self._search_for_flag("_is_overriding")

        def get_attr(base, ref):
            yield from map(partial(getattr, base),
                filter(lambda x: x==ref, dir(base))
            )

        for attrib in filter(callable, attribs):
            sig = attrib.__name__
            attrib_sig = signature(attrib)

            for base in self.__bases__:
                for attr in filter(callable, get_attr(base, sig)):
                    if signature(attr) == attrib_sig:
                        return
            else:
                assert False, f"{attrib} does not override anything"

    def __init__(self) -> None:
        if __debug__: self._check_overload()


class Singleton(ClassUtils):

    def __new__(cls, *args, **kwargs) -> "Singleton":
        assert not hasattr(cls, "_instance"), \
            f"An instance of {cls} already exists"
        return super().__new__(cls)

    @classmethod
    def instance(cls, *args, **kwargs) -> "Singleton":

        def dummy_instance(*args, **kwargs):
            return cls._instance

        cls._instance = cls(*args, **kwargs)
        cls.instance = dummy_instance
        return cls._instance


class ClassRegistry(ABCMeta, ClassUtils):

    _DATABASE = dict()

    def __new__(self, name, bases, namespace, **kwargs):
        return ABCMeta.__new__(self, name, bases, namespace)


    def __init__(self, name, bases, namespace, **kwargs):
        ABCMeta.__init__(self, name, bases, namespace)
        ClassUtils.__init__(self)

        self._DATABASE[kwargs.get("id", name)] = self



    