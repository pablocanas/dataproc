__author__ = 'fran'

import threading


def synchronized(method):
    def f(*args):
        self = args[0]
        self.mutex.acquire()
        # print(method.__name__, 'acquired')
        try:
            return apply(method, args)
        finally:
            self.mutex.release()
            # print(method.__name__, 'released')
    return f


def synchronize(klass, names=None):
    """Synchronize methods in the given class.
    Only synchronize the methods whose names are
    given, or all methods if names=None."""
    if type(names)==type(''): names = names.split()
    for (name, val) in klass.__dict__.items():
        if callable(val) and name != '__init__' and (names is None or name in names):
            # print("synchronizing", name)
            klass.__dict__[name] = synchronized(val)


# You can create your own self.mutex, or inherit
# from this class:
class Synchronization:
    def __init__(self):
        self.mutex = threading.RLock()