# Test runtime here
import time
start_time = time.perf_counter()

def time_test(f, *args, **kwargs) -> float:
    '''
    Function designed to test other function runtimes.\n
    Can also print output of tested funtion through bool.
    '''
    if hasattr(f, '__call__'): # check if function can be called
        start_time = time.perf_counter()
        f(*args) # unpack input arguments
        end_time = time.perf_counter()

        if kwargs.get('prints'):
            print(f"{f.__name__}: {end_time - start_time} seconds")
        return end_time - start_time
