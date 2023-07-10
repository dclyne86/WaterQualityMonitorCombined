
# ## Importing Data

#
# -*- coding: utf-8 -*-
# Regression Example With Boston Dataset: Standardized and Wider
import os
import functions

from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

import numpy as np
import pandas as pd


import tensorflow as tf
import cloudinary
import cloudinary.api
import requests
import shutil
import sql_manager

import os


tf.keras.optimizers.RectifiedAdam = Adam
k_folds = functions.get_num_folds()

optimal_NNs = [None]*k_folds
integrals = 0.
time, pH, current, temperature = [], [], [], []
longest_range_for_diff = 26

def manage_data(currTime, curCurrent, switchOn):
    global integrals, time, current, pH, temperature

    if not switchOn and currTime < 50:
        time = []
        integrals = 0.0
        return integrals

    if currTime % 1 == 0:
        currTime -= 50
        time.append(currTime)
        current.append(curCurrent)
        pH.append(predict_pH(time, ))

    if len(time) >= longest_range_for_diff:
        integrals = getIntegrals(time, current)

    return integrals

def getIntegrals(time, current):
    integrals = np.trapz(time[:longest_range_for_diff], current[:longest_range_for_diff])
    return integrals

def filterData():

    grads = np.grad(current)
    if len(time) >= 50:
        l = 0
        r = l + 1

        for cg in grads:
            if cg[l] > cg[r]:
                r +=1
                if (r - l) == longest_range_for_diff:
                    integrals = np.trapz(time[l:r], current[l:r])

                if (r - l) >= longest_range_for_diff:
                    if cg[r] == cg[-1]:
                        return np.array([time[l:r], current[l:r], pH[l:r], temp[l:r]])

            else:
                l+=1
                r = l +1

    return 0

def uploadtoCloud(concentration):
    table_name = sql_manager.get_table_name()
    engine = sql_manager.connect()

    # if len(time) >= 50:
    tmp = np.ones(len(time))

    entry = np.array([np.asarray(time), np.asarray(current), np.asarray(pH), np.asarray(temperature), tmp, tmp*integrals])
    return entry
        # pd.DataFrame(entry, columns=['Time', 'Current','pH', 'Temp', 'Rinse', 'Integrals', 'Concentration'])
    #
    #
    # if not sql_manager.check_tables(engine, table_name):
    #     pandas_to_sql(table_name, sensor_data, engine)
    # else:
    #
    #     pandas_to_sql(table_name, sensor_data, engine)


    return 1


def download_models():
    global optimal_NNs
    zip_public_id = f'{functions.get_model_folder_name()}.zip'  # Or provide the URL of the ZIP file
    # Get the download URL for the ZIP file from Cloudinary
    download_url = cloudinary.utils.cloudinary_url(zip_public_id,
                                                   resource_type='raw')[0]

    response = requests.get(download_url, stream=True)

    path = os.path.join(os.environ['HOME'],
                        f'{zip_public_id}')

    with open(path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)

    shutil.unpack_archive(path, os.environ['HOME'])

    i = 0

    for filename in os.listdir(os.environ['HOME']):
        if "Model " in filename and ".h5" in filename:
            optimal_NNs[i] = load_model(os.path.join(os.environ['HOME'], f'{filename}'), compile=False)

            i += 1

    return str(optimal_NNs)

def predict_Cl(time, current, pH, temp, integrals):


    sensor_data = np.array([[time, current, pH, temp, 1, integrals]])
    sensor_data = pd.DataFrame(sensor_data,
                                columns=['Time', 'Current','pH', 'Temp', 'Rinse', 'Integrals'])


    k_folds = functions.get_num_folds()
    tmp_ppm = [None]*k_folds
    # return  sensor_data
    for fold in range(k_folds):
        tmp_ppm[fold] = functions.predict_ppm(optimal_NNs[fold], sensor_data)

    return sum(tmp_ppm)[0][0]/k_folds

def predict_pH(time, rawpH):
    #insert model preduction here
    return rawpH

def predict_T(time, rawT):
    #insert model preduction here
    return rawT





