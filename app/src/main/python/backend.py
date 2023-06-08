
# ## Importing Data

#
# -*- coding: utf-8 -*-
# Regression Example With Boston Dataset: Standardized and Wider
import os
import functions

from tensorflow import keras
import numpy as np
import file_management


k_folds = functions.get_num_folds()
optimal_NNs = [None]*k_folds
def download_models():
    global optimal_NNs

    path = file_management.get_file_path()

    functions.load_from_cloud()
    local_download_path = os.path.join(os.environ['HOME'], f'{path}')

    i = 0
    for filename in os.listdir(local_download_path):

        if "Model" in filename:
            #optimal_NNs[i] = load_model(f"{path}\\{filename}")
            # TODO there could be some bugs here
            optimal_NNs[i] = keras.load_model(os.path.join(os.environ['HOME'], f'{path}\\{filename}'))


            #print(optimal_NNs[i].optimizer)
            i+=1


    return


def predict_Cl(time, current, pH, temp, integrals):

    sensor_data = np.array([time, current, pH, temp, integrals])
    k_folds = functions.get_num_folds()
    tmp_ppm = [None]*k_folds
    for fold in range(k_folds):
        tmp_ppm[fold] = functions.predict_ppm(optimal_NNs[fold], sensor_data)

    return sum(tmp_ppm)/k_folds







