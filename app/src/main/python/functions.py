
import secret

import cloudinary
import cloudinary.api
import requests
import shutil

import os

def get_model_folder_name():
    return "gold_fc_h5"

def get_table_name():
    return 'gold_fc'

def get_std_params_table_name():
    return 'std_params_gold'

def get_data_folder_name():
    return "Data"

def get_num_folds():
    return 3

def predict_ppm(model, features):
    return model.predict(features)



