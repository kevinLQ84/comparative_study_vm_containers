'''
Program to take in JSON files created from 'runtime_data_gatherer'.
Output graphs with other consolidated data, such as mean, median, mode, range and many others.
Consideration of output values:
    - graph data of various execution times
    - mean
    - median
    - mode, may be difficult due to highly variable exeution time
    - range, highest execution time and lowest execution time
'''
from json_functs import create_json
import json
import matplotlib.pyplot as plt

def process_json(filename: str, *args, **kwargs) -> dict:
    '''
    Read a file and assume it is JSON.\n
    It can either average the results or not.\n
    Return the file as a processed version.\n
    kwargs are average_all_results.
    '''
    results_dict = {}

    # assume filename goven is a JSON file
    with open(filename, 'r') as openfile:
        raw_json_file: dict = json.load(openfile)
        # eg {funct: [{input: time, input2: time2}, {input: time, input2: time}]}

    # if multiple sets of runtimes used, they should be automatically averaged
    # otherwise a graph will be made for each set of runtimes
    average_all_results = True
    if kwargs.get("average_all_results") == False:
        average_all_results = False

    if average_all_results:
        # iterate over each of the functions used
        for funct in raw_json_file.keys():
            results_dict[funct] = {}    # prepare to store averaged results
            n_to_average = len(raw_json_file[funct]) # number of items to be averaged
            # iterate through the list of runtimes
            # runtime is a dictionary with keys of input and values of time taken
            runs: list = raw_json_file[funct]
            # data is a runtime recorded as a dictionary
            for raw_data_dict in runs:   # each raw_data is a dictionary of a runtime
                raw_data_dict: dict
                for result in raw_data_dict.keys(): # iterate through the current runtime dict
                    # check if there's a value already inside our averaged data
                    if results_dict[funct].get(result) == None:
                        results_dict[funct][result] = 0
                    results_dict[funct][result] += raw_data_dict[result]
            # assume each dictionary of the list in raw_json_file have same key values
            # average them based on length of the list
            for result in results_dict[funct].keys():
                averaged_result = results_dict[funct][result]/n_to_average
                results_dict[funct][result] = round(averaged_result, 4)
        # create json file for averaged results
        create_json(results_dict, name = 'avg_data.json')
    else:
        # instead of averaging results, only one set from the list is done
        # this entirely skips all other runs and uses only the first
        # each function has a list with only one dictionary
        for funct in raw_json_file.keys():
            results_dict[funct] = {}    # prepare to store non-averaged results
            raw_data_dict: dict = raw_json_file[funct][0]
            for raw_result in raw_data_dict.keys():
                # place input value as key and runtime as value
                results_dict[funct][raw_result] = raw_data_dict[raw_result] 

    return (results_dict)

def graph_generate(results: dict, *args, **kwargs) -> None:
    '''
    Generate a graph based on a JSON file containing runtime data.
    Return the dictionary used to produce the graph
    '''
    plt.rcParams.update({'font.size': 5})
    # get x axis and y axis values
    x = [] # inputs
    y = [] # time taken
    functions = [i for i in results.keys()] 
    for funct in functions:
        for input in results[funct].keys():
            x.append(input)
            y.append(results[funct][input])
    # print(x, y)
    
        # generate the graph
        plt.plot(x, y, \
                 label = f'{funct}', marker='o', markerfacecolor='blue', markersize=5) 
        plt.xlabel('matrix size (NxN)') 
        plt.ylabel('time (seconds)') 
    
    plt.title('Function Runtime')
    plt.legend()  
    plt.show() 
                
if __name__ == '__main__':
    print(graph_generate(process_json('data.json'), average_all_results = False))


