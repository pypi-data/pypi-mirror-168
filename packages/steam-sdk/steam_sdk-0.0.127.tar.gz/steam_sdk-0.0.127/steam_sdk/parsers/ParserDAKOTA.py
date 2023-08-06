import os
from pathlib import Path

from steam_sdk.data.DataDakota import DataDakota
from steam_sdk.parsers.ParserYAML import yaml_to_data


class ParserDakota:
    """
        Class with methods to read/write FiQuS information from/to other programs
    """

    def __init__(self, input_DAKOTA_data_yaml, verbose: bool = True):
        """
            Initialization using a BuilderDAKOTA object containing DAKOTA parameter structure
            Read the DAKOTA input variables from a input_DAKOTA_data_yaml file and parse into the object

        """
        self.dakota_data = yaml_to_data(full_file_path=input_DAKOTA_data_yaml, data_class=DataDakota)

        if verbose:
            print('File {} was loaded.'.format(input_DAKOTA_data_yaml))

    def writeDAKOTA2in(self, output_file_full_path: str, verbose: bool = False):
        """
        Writes the DAKOTA object into a respective .in file according to the format
        """

        # If the output folder is not an empty string, and it does not exist, make it
        output_path = os.path.dirname(output_file_full_path)
        if verbose:
            print('output_path: {}'.format(output_path))
        if output_path != '' and not os.path.isdir(output_path):
            print("Output folder {} does not exist. Making it now".format(output_path))
            Path(output_path).mkdir(parents=True)

        dict_to_in(self.dakota_data.DAKOTA_analysis.dict(), output_file_full_path)

def dict_to_in(data_dict, name_output_file: str):
    '''
    Function that converts a dictionary into a .in file for DAKOTA

    :param data_dict, dict - contains all keys and values
    :param name_output_file, str - name of the .in file
    '''

    def __fill_up_level(level: int, string: str):
        '''
        Helper function that fills up a string with a tabular, according to the level
        '''
        filler = ''.join(map(str,([' ']*level*4)))
        return filler + string

    def __flatten_list(list: list):
        '''
        Helper function that reduces a list to a single string, separated by one space
        '''
        list = ["'"+x+"'" if type(x)==str else x for x in list]
        return ' '.join(map(str,list))

    def __construct_string(data, key):
        '''
        Helper function that constructs a string from data values, based on the type
        '''
        # If data value is empty/false: ignore
        if not data[key]:
            return ''

        # If string: fill only with data value
        if type(data[key]) == str:
            string = f"{key} = '{data[key]}' \n"
        # If list: return list flattened to a single line
        elif type(data[key]) == list:
            string = f"{key} = {__flatten_list(data[key])} \n"
        # If bool: return only key, without it's value
        elif type(data[key]) == bool:
            string = f"{key} \n"
        # All other types: return key and value
        else:
            string = f"{key} = {data[key]} \n"
        # Convention: If key is marked as a type, we ignore the key and just return the value
        if 'type' in key:
            string = f"{data[key]} \n"
        return string

    # Actual function that writes the .in file
    with open(name_output_file, 'w') as in_file:
        # Loop through all DAKOTA key words
        for key in data_dict.keys():
            in_file.write(f'{key} \n')
            # Loop through all sub-keys in each category
            for subkey in data_dict[key].keys():
                if type(data_dict[key][subkey])==dict:
                    for subsubkey in data_dict[key][subkey].keys():
                        string = __construct_string(data_dict[key][subkey], subsubkey)
                        if string: in_file.write(__fill_up_level(2, string))
                else:
                    string = __construct_string(data_dict[key], subkey)
                    if string: in_file.write(__fill_up_level(1, string))