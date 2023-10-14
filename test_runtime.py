# Test runtime here
import time
start_time = time.perf_counter()

def time_test(f, *args, **kwargs) -> float:
    '''
    Test other function runtimes.\n
    Can also print output of tested funtion through bool.\n
    First argument must always be a function.
    '''
    if hasattr(f, '__call__'): # check if function can be called
        # support functionality for obtaining averages
        loops = 1
        avg = 0
        if kwargs.get('n_runs_on_average'):
            loops = kwargs.get('n_runs_on_average')
        for i in range(loops):
            start_time = time.perf_counter()
            f(*args) # unpack input arguments
            end_time = time.perf_counter()
            avg += end_time - start_time
        # finalise runtime
        runtime = avg/loops
        
        # output time if requested
        if kwargs.get('prints'):
            print(f"{f.__name__}: {runtime} seconds")
        return end_time - start_time
    
    return None
