import functools
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Callable

"""
The following imports are going to be accessible by the user
as all hacked methods are invoked from here
"""
# TODO: this is to be replaced with level-defined imports

from grid.grid import Grid
grid = Grid()


class MethodInfoDict(ABC):
    @staticmethod
    @abstractmethod
    def get_meth_info():
        pass

    @classmethod
    def get_all_methods_of_class(cls, owner_class):
        return cls.get_meth_info()[owner_class.__name__]


class ReadOnlyMethod(MethodInfoDict):
    meth_info = defaultdict(list)

    @staticmethod
    def get_meth_info():
        return ReadOnlyMethod.meth_info

    def __init__(self, meth: Callable):
        """
        Inserts the default body of a hackable method to meth_info dictionary.
        """
        self.class_name, self.meth_name = meth.__qualname__.rsplit('.', 1)
        ReadOnlyMethod.meth_info[self.class_name].append(self.meth_name)
        self._meth = meth

    def __call__(self, instance, owner, *args, **kwargs):
        """
        Overrides the decorated method call. Calls the version stored in meth_info instead.
        :param instance: Calling object instance
        :param owner: Calling object type
        :return: What the hacked method returns
        """
        return self._meth(instance, *args, **kwargs)




class CallableMethod(MethodInfoDict):
    meth_info = defaultdict(list)

    @staticmethod
    def get_meth_info():
        return CallableMethod.meth_info

    def __init__(self, meth: Callable):
        """
        Inserts the default body of a hackable method to meth_info dictionary.
        """
        self.class_name, self.meth_name = meth.__qualname__.rsplit('.', 1)
        print(self.class_name, self.meth_name)
        CallableMethod.meth_info[self.class_name].append(self.meth_name)
        self._meth = meth
        self.hacker_accessible = True

    def __call__(self, instance, owner, *args, **kwargs):
        """
        Overrides the decorated method call. Calls the version stored in meth_info instead.
        :param instance: Calling object instance
        :param owner: Calling object type
        :return: What the hacked method returns
        """
        return self._meth(instance, *args, **kwargs)

    def __get__(self, instance, owner):
        """
        Executes before __call__ when the method is called. Provides __call__ with access
        to the calling instance and type.
        """
        return functools.partial(self.__call__, instance, owner)


class HackableMethod(MethodInfoDict):
    """
    A class-decorator used to describe a method, the code of which can be altered by the user.
    When creating new Entities, use
    @HackableMethod
    def do_stuff(self, arg1):
        <default_body>
    """

    # A static dictionary containing the overwritten methods
    meth_info = defaultdict(dict)
    hacker_scope = False

    @staticmethod
    def get_meth_info():
        return HackableMethod.meth_info

    def __init__(self, meth: Callable, imports=None):
        """
        Inserts the default body of a hackable method to meth_info dictionary.
        """
        self.class_name, self.meth_name = meth.__qualname__.rsplit('.', 1)
        print(self.class_name, self.meth_name)
        HackableMethod.meth_info[self.class_name][self.meth_name] = meth
        self._default_meth = meth
        self.hacker_accessible = True

    def __call__(self, instance, owner, *args, **kwargs):
        """
        Overrides the decorated method call. Calls the version stored in meth_info instead.
        :param instance: Calling object instance
        :param owner: Calling object type
        :return: What the hacked method returns
        """
        HackableMethod.hacker_scope = True
        val = HackableMethod.meth_info[self.class_name][self.meth_name](instance, *args, **kwargs)
        HackableMethod.hacker_scope = False
        return val

    def __get__(self, instance, owner):
        """
        Executes before __call__ when the method is called. Provides __call__ with access
        to the calling instance and type.
        """
        return functools.partial(self.__call__, instance, owner)

    @staticmethod
    def apply_code(code: str, self_instance):
        """
        Applies the given code to overwrite the hackable methods of the inheriting class
        """
        class_name = self_instance.__class__.__name__
        hackable_method_names = self_instance.get_hackable_method_names()

        scope = {"self": self_instance}

        # “As for the end of the universe...
        # I say let it come as it will, in ice, fire, or darkness.
        # What did the universe ever do for me that I should mind its welfare?”
        HackableMethod.hacker_scope = True
        print(code)
        exec(code, None, scope)
        HackableMethod.hacker_scope = False

        for var_name, var_value in scope.items():
            if var_name in hackable_method_names:
                HackableMethod.meth_info[class_name][var_name] = var_value