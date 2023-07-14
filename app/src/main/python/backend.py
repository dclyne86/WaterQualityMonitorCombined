
# ## Importing Data

#

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
time, all_pH, current, temperature = [], [], [], []
concentration = []
longest_range_for_diff = 26
predictedFcl = 0

def correctCl(rawI):
    offset = 0.109

    corrected = -rawI + offset
    return corrected



def manage_data(currTime, curCurrent, pH, T, switchOn):
    global integrals, time, current, all_pH, temperature, concentration

    if not switchOn and currTime < 50:
        time = []
        all_pH = []
        temperature = []
        current = []
        integrals = 0.0
        concentration = []
        return integrals

    if currTime % 1 == 0:
        currTime -= 50
        time.append(currTime)
        current.append(correctCl(curCurrent))
        all_pH.append(7)
        temperature.append(30)
        concentration.append(predictedFcl)

    if len(time) >= longest_range_for_diff:
        integrals = getIntegrals(time, current)

    return integrals

def getIntegrals(time, current):
    return -np.trapz(time[:longest_range_for_diff], current[:longest_range_for_diff])

def uploadtoCloud():
    table_name = sql_manager.get_table_name()
    engine = sql_manager.connect()


    entry = []
    if len(time) >= longest_range_for_diff:
        tmp = np.ones(len(time))

        entry = np.array([np.asarray(time), np.asarray(current), np.asarray(all_pH), np.asarray(temperature), tmp, tmp*integrals, concentration])
        df = pd.DataFrame(entry.T, columns=['Time', 'Current','pH', 'Temp', 'Rinse', 'Integrals', 'Concentration'])

        if df['Time'][len(df)-1] >= 50:
            if not sql_manager.check_tables(engine, table_name):
                sql_manager.pandas_to_sql(table_name, df, engine)
                return "Created new Table"
            else:
                sql_manager.pandas_to_sql_if_exists(table_name, df, engine, 'append')
                return "Appended to Table"
        return df

    return "pending"


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
    global predictedFcl

    if integrals == 0:
        return 0

    sensor_data = np.array([[time, correctCl(current), pH, 30, 1, integrals]])
    sensor_data = pd.DataFrame(sensor_data,
                                    columns=['Time', 'Current','pH', 'Temperature', 'Rinse', 'Integrals'])

    k_folds = functions.get_num_folds()
    tmp_ppm = [None]*k_folds
    # return  sensor_data
    for fold in range(k_folds):
        tmp_ppm[fold] = functions.predict_ppm(optimal_NNs[fold], sensor_data)

    predictedFcl = sum(tmp_ppm)[0][0]/k_folds
    return predictedFcl

def predict_pH(time, rawpH):
    #insert model preduction here
    return rawpH

def predict_T(time, rawT):
    #insert model preduction here
    return rawT





