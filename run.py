'''
file to run other modules

For simplicity of the report, only matrix multiplication will be used.
'''
import runtime_data_gatherer as rdg
import runtime_data_finaliser as rdf
import random
import sys

# set a fixed seed for random output
random.seed(10)

if __name__ == '__main__':
    '''
    parameters
    seed is 10.
    start on 20x20 to 300x300 matrices with step 20.
    averaged on 10 runs.
    '''
    sys.setrecursionlimit(2500)
    rdg.create_json(rdg.run_functions(20, 300, 20, n_runs = 10))
    rdf.graph_generate(rdf.process_json('data.json'))

