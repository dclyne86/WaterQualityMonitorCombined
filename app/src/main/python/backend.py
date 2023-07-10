
# ## Importing Data

#
# -*- coding: utf-8 -*-
# Regression Example With Boston Dataset: Standardized and Wider
import os
import functions

from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

import numpy as np

import tensorflow as tf
import cloudinary
import cloudinary.api
import requests
import shutil

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

    if len(time) >= longest_range_for_diff:
        integrals = getIntegrals(time, current)

    return integrals

def getIntegrals(time, current):
    integrals = np.trapz(time[:longest_range_for_diff], current[:longest_range_for_diff])
    return integrals

def filterData():
    if len(time) >= 50:
        l = 0
        r = len(time) - 1
        for
    for i in time:


    return 0

def uploadtoCloud():

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

    import pandas as pd
    sensor_data = pd.DataFrame(sensor_data,
                                columns=['Time', 'Current','pH', 'Temp', 'Rinse', 'Integrals'])


    k_folds = functions.get_num_folds()
    tmp_ppm = [None]*k_folds
    # return  sensor_data
    for fold in range(k_folds):
        tmp_ppm[fold] = functions.predict_ppm(optimal_NNs[fold], sensor_data)

    return sum(tmp_ppm)[0][0]/k_folds

# def predict_pH(time, pH,):
#     #insert model preduction here
#     return 0
#
# def predict_T(time, pH,):
#     #insert model preduction here
#     return 0





