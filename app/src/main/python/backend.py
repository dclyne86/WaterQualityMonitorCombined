
# ## Importing Data

#
# -*- coding: utf-8 -*-
# Regression Example With Boston Dataset: Standardized and Wider
import os
import functions

from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

import numpy as np
import file_management

import tensorflow as tf


tf.keras.optimizers.RectifiedAdam = Adam
k_folds = functions.get_num_folds()
optimal_NNs = [None]*k_folds
integrals = 0.
time, pH, current, temperature = [], [], [], []
longest_range_for_diff = 26

def transform_data(currTime, curCurrent, switchOn):
    global integrals, time

    if not switchOn and currTime < 50:
        time = []
        integrals = 0.0
        return time, integrals

    if currTime % 1 == 0:
        currTime -= 50
        time.append(currTime)
        current.append(curCurrent)

    if len(time) >= longest_range_for_diff:
        integrals = np.trapz(time[:longest_range_for_diff], current[:longest_range_for_diff])

    return time, integrals

def download_models():
    global optimal_NNs

    path = file_management.get_file_path()

    file_name = functions.get_model_folder_name()

    i = 0
    for filename in os.listdir(os.environ['HOME']):
        if "Model " in filename:
            optimal_NNs = load_model(os.path.join(os.environ['HOME'], f'{filename}'))
            return optimal_NNs.optimizer
            # optimal_NNs[i] = load_model(f".\\{folder_name}\\{filename}")
            # print(optimal_NNs[i].optimizer)
            # tmp = re.findall(r'\d+', filename)
            # i+=1


            # optimal_NNs[i] = load_model(os.path.join(os.environ['HOME'], f'{filename}') , optimizer=Adam(lr=0.001, decay=1e-5))
            # optimal_NNs[i] = load_model(os.path.join(os.environ['HOME'], f'{filename}'), compile = False)
            i += 1


    # return str(optimal_NNs)

    # local_download_path = , f'{path}')

    # for filename in os.path.join(os.environ['HOME'], f'{path}'):
    #     return filename
    #
    #     if "Model" in filename:
    #         #optimal_NNs[i] = load_model(f"{path}\\{filename}")
    #         # TODO there could be some bugs here
    #         optimal_NNs[i] = keras.load_model(os.path.join(os.environ['HOME'], f'{path}\\{filename}'))
    #
    #
    #         #print(optimal_NNs[i].optimizer)
    #         i+=1
    # i = 0
    # functions.load_from_cloud(k_folds)
    # file_name = functions.get_model_folder_name()



def predict_Cl(time, current, pH, temp, integrals):

    sensor_data = np.array([time, current, pH, temp, integrals])
    k_folds = functions.get_num_folds()
    tmp_ppm = [None]*k_folds
    for fold in range(k_folds):
        tmp_ppm[fold] = functions.predict_ppm(optimal_NNs[fold], sensor_data)

    return sum(tmp_ppm)/k_folds







