import os

from steam_sdk.parsers.ParserYAML import dict_to_yaml
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing


class ParserFiQuS:
    """
        Class with methods to write FiQuS input files from steam sdk
    """

    def __init__(self, builder_FiQuS, verbose=True):
        """
        Initialization using a BuilderFiQuS object containing FiQuS parameter structure
        :param builder_FiQuS: BuilderFiQuS object
        :param verbose: boolean if set to true more information is printed to the screen
        """

        self.builder_FiQuS = builder_FiQuS
        self.verbose = verbose

        if self.builder_FiQuS.data_FiQuS.magnet.type == 'multipole':
            self.attributes = ['data_FiQuS', 'data_FiQuS_geo', 'data_FiQuS_set']
            self.file_exts = ['yaml', 'geom', 'set']
        elif self.builder_FiQuS.data_FiQuS.magnet.type == 'CCT':
            self.attributes = ['data_FiQuS']
            self.file_exts = ['yaml']
        else:
            raise Exception(f'Magnet type {self.builder_FiQuS.data_FiQuS.magnet.type} is incompatible with FiQuS.')

    def writeFiQuS2yaml(self, output_path: str, append_str_to_magnet_name: str = ''):
        """
        ** Writes FiQuS input files **

        :param output_path: full path to output folder.
        :param append_str_to_magnet_name: additional string to add to magnet name, e.g. '_FiQuS'.
        :return:   Nothing, writes files to output folder.
        """

        make_folder_if_not_existing(output_path)  # If the output folder is not an empty string, and it does not exist, make it
        for attribute, file_ext in zip(self.attributes, self.file_exts):
            dict_to_yaml(getattr(self.builder_FiQuS, attribute).dict(),
                         os.path.join(output_path, f'{self.builder_FiQuS.data_FiQuS.general.magnet_name}{append_str_to_magnet_name}.{file_ext}'), list_exceptions=[])


