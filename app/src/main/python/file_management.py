import functions
import os

def get_file_path():
    folder_name = functions.get_model_folder_name()
    return os.path.join(os.environ['HOME'], f'{folder_name}')

def get_data_path():
    folder_name = functions.get_data_folder_name()
    return os.path.join(os.environ['HOME'], f'{folder_name}')
