#!/usr/bin/env python3


# Will run wherever it's called. Meant to be global util. 
# Can also be used as normal imported lib
# Possible usage, python: 
# ```
# import xxx
# xxx.main(directory)
# ```
# bash: template or ./template
# bash: template <args> 
#
# Various utils to save time when writing loops or other nested conditionals.

    
import sys
sys.path.append("/home/blue/Projects/utils/")
from filesystem_utils import *
import time

# @persistent() decorator object.
"""
SEE HERE FOR INFO ON WEIRD DECORATOR-FU

Apparently we need 3 levels of nesting to have the decorator have args, take a function, 
and allow the function its wrapping to have arguments too.
    This is for if the decorator is used like @decorator(), or @decorator(1) .

However if we don't pass the decorator an argument, and want it to have an optional one,
we HAVE to have only two levels of nesting. 
    This is for if the decorator is used like @decorator .

Fortunately once we figure out how to balance it so we can get *both*, it still works with the
    decorated function regardless of what arguments and how many arguments that function has.

I did test this, with the three cases of decorator @decorator, @decorator(), @decorator(x),
    alongside a decorated function with the three cases of test(x,y), test(x), test().

All in all it was 9 combinations, all working now.
"""

# decorator
def persistent(interval=0):
    """
    This decorator will not modify any of the behavior of `func` passed to it.
        Instead, it will simply make sure it runs forever, with the only exception being
        user interruption (KeyboardInterrupt). Otherwise it will create an infinite loop,
        with an optional argument for intervals to wait between loops `interval`.

    It calls the function per usual, but if any Exceptions arise, it will print the traceback
        and start the function again after optional `interval` time has passed. 

    It WILL NOT error out and cause unexpected interruption of the program, 
        UNLESS it is interrupted by the user via a KeyboardInterrupt Exception.

    Note: this is our own Super Decorator, which means your interpreter might say it has errors,
        but in reality we're smarter than your interpreter and it actually works. So ignore them.

    If you're running this, you don't care about if it gets possibly spammed. Use with care.
    """
    # Assume called conventionally, like @decorator / @persistent
    conventional_decorator = type(interval) != int and type(interval) != float

    # Main decorator code. Has one special flag to ensure we have the correct function.
    def wrapper_with_args_and_function(*args, **kwargs):

        if "__decorated_f__" in kwargs:
            # Sneakily smuggle the decorated function despite Python's best wishes
            decorated_f = kwargs["__decorated_f__"]
            del kwargs["__decorated_f__"]

        while True:
            try:
                decorated_f(*args, **kwargs)
            except KeyboardInterrupt:
                print("Termination Requested by User. Stopping...")
                sys.exit()
            except Exception as e:
                print("Exception encountered:")
                print(traceback.format_exc())
            time.sleep(interval)


    if conventional_decorator:
        # Get the function
        decorated_f = interval

        # Default interval 0 if called like @persistent rather than @persistent()
        interval = 0

        # Only two layers of nesting for conventional decorator
        def wrapper_with_args(*args, **kwargs):
            return wrapper_with_args_and_function(*args, **kwargs, __decorated_f__=decorated_f)

        return wrapper_with_args

    else:
        # Three layers of nesting for decorator with args.
        def wrapper(decorated_f):
            def wrapper_with_args(*args, **kwargs):
                return wrapper_with_args_and_function(*args, **kwargs, __decorated_f__=decorated_f)
            return wrapper_with_args
        return wrapper
