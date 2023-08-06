import os

from .general import emojis
from .decorator import _list
from .general import path_join

@_list
def mkdir(dir_list):
    for dir in dir_list:
        dirs = []
        while True:
            if not os.path.exists(dir) and dir != '':
                arr = os.path.normpath(dir).split(os.sep)
                dirs.insert(0, arr[-1])
                dir = path_join(arr[:-1])
            else:
                for i in range(len(dirs)):
                    os.mkdir(path_join([dir, dirs[:i+1]]))
                break

import contextlib

class TryExcept(contextlib.ContextDecorator):
    """
    Example:
    @TryExcept('⚠️ nani the fck: ')
    def calculate(x):
        return x/0
    """
    def __init__(self, msg=''):
        self.msg = msg

    def __enter__(self):
        pass

    def __exit__(self, exc_type, value, traceback):
        if value:
            print(emojis(f'{self.msg}{value}'))
        return True