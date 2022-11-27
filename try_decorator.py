import pdb
from functools import wraps


def only_ints(fn):
    @wraps(fn)
    def wrapper(*args):
        #        pdb.set_trace()
        for val in args:
            if type(val) != int:
                return "Please invoke with integers."
        return fn(*args)

    return wrapper


@only_ints
def add(x, y):
    z = x + y
    return z


print(add('1', 2))
