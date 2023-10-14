''' 
file to store shared json functions
'''
import json
def create_json(dictionary: dict, *args, **kwargs) -> None:
    '''
    Generate a JSON file for storing results.
    kwargs are name.
    '''
    filename = 'data.json'
    # check for custom name
    if kwargs.get('name'):
        filename = kwargs['name']

    # serialize json file
    json_file = json.dumps(dictionary, indent=4) # indent for readability

    # write to file
    # will overwrite any previous data
    with open(filename, 'w') as output_file:
        output_file.write(json_file)

if __name__ == '__main__':
    pass