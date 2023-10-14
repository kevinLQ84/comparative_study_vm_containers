'''
program to use a specified list of python programs listed inside.
there should be a default seed to test random numbers
execution output should be placed in a folder in JSON formatting
'''
from json_functs import create_json
from test_runtime import time_test
from matrix_multiplication import matrix_multi_simple
import json

def run_functions(*args, **kwargs) -> dict:
    '''
    Run a given list of functions and return a dict of results.\n
    By default only matrix multiplication is used.\n
    * args are start, end, step.\n
    * kwargs are functs, n_runs.
    '''
    functions = [matrix_multi_simple]
    # args
    if args == ():
        # default input
        int_inputs = [1, 10, 20, 50, 100]
    else:
        # generate int_inputs from args
        # if args is [0, 100, 50], then list generated should be
        # assuming arg input is 3 numbers, 0, 100 and 50 then list is [0, 50, 100]. Any number beyond 100 is discarded
        start_input_value, max_input_value, input_steps = args[0], args[1], args[2]
        int_inputs = [x for x in range(start_input_value, max_input_value+1, input_steps)]
    # kwargs
    if kwargs.get('functs') == type(list):
        # assumes parsed in list contains functions
        functions = kwargs['functs']

    # number of runs to be repeated
    n_runs = 1
    if kwargs.get('n_runs'):
        n_runs = kwargs['n_runs']

    # dict of outputs from time_test mapped to the function it was used on
    # with the funct, the runtimes are stored for each set of executions stored in a list
    # eg {funct: [{input: time, input2: time2}, {input: time, input2: time}]}
    time_dict = {}

    for funct in functions:
        # function key holds inputs and runtimes
        time_dict[funct.__name__] = []
        for run in range(n_runs):
            # create a pointer to the current run
            current_run = {}
            time_dict[funct.__name__].append(current_run)
            # place runtimes in current run with input args matched to runtime
            for input in int_inputs:
                time_taken = time_test(funct, input)
                current_run[input] = round(time_taken, 4)

    return time_dict
    
if __name__ == '__main__':
    # print out the function and it's input with the resulting runtime
    start = 50
    end = 200
    step = 50
    runs = 5
    results = run_functions(start, end, step, n_runs = runs)
    create_json(results)

    # pretty print results
    for item in results.keys():
        print(f'funct: [{item}]')
        runtimes: list = results[item] # a list of runtimes containing dictionaries
        runs = 1
        for d in runtimes: # iterate through each of the function's runtimes
            print(f'run {runs}:')
            for input in d.keys(): # extract keys
                print(f'{"":<5}{input:^4}:{"":<5}{d[input]} seconds')
            runs+=1
            print()