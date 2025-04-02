import functools
from collections import defaultdict
from typing import Callable

"""
The following imports are going to be accessible by the user
as all hacked methods are invoked from here
"""
# TODO: this is to be replaced with level-defined imports
from random import random, randint
from grid.position import Position
from grid.grid import Grid
grid = Grid()



class HackableMethod:
    """
    A class-decorator used to describe a method, the code of which can be altered by the user.
    When creating new Entities, use
    @HackableMethod
    def do_stuff(self, arg1):
        <default_body>
    """

    # A static dictionary containing the overwritten methods
    meth_info = defaultdict(dict)

    def __init__(self, meth: Callable, imports=None):
        """
        Inserts the default body of a hackable method to meth_info dictionary.
        """
        self.class_name, self.meth_name = meth.__qualname__.rsplit('.', 1)
        print(self.class_name, self.meth_name)
        HackableMethod.meth_info[self.class_name][self.meth_name] = meth
        self._default_meth = meth

    def __call__(self, instance, owner, *args, **kwargs):
        """
        Overrides the decorated method call. Calls the version stored in meth_info instead.
        :param instance: Calling object instance
        :param owner: Calling object type
        :return: What the hacked method returns
        """
        return HackableMethod.meth_info[self.class_name][self.meth_name](instance, *args, **kwargs)

    def __get__(self, instance, owner):
        """
        Executes before __call__ when the method is called. Provides __call__ with access
        to the calling instance and type.
        """
        return functools.partial(self.__call__, instance, owner)

    @staticmethod
    def get_all_hackable_methods(owner_class):
        """
        Returns all hackable methods for a given type.
        :param owner_class: The type.
        :return: A dict of (method_name: method) pairs.
        """
        return HackableMethod.meth_info[owner_class.__name__]

    @staticmethod
    def apply_code(code: str, class_name: str, hackable_method_names: list[str]):
        """
        Applies the given code to overwrite the hackable methods of the inheriting class
        """
        scope = {}
        # “As for the end of the universe...
        # I say let it come as it will, in ice, fire, or darkness.
        # What did the universe ever do for me that I should mind its welfare?”
        exec(code, None, scope)
        for var_name, var_value in scope.items():
            if var_name in hackable_method_names:
                HackableMethod.meth_info[class_name][var_name] = var_value