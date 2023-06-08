
import secret

import cloudinary
import cloudinary.api
import requests
# import shutil
import os
import file_management

def get_dict(tt_feats):
    dict = {
        'Time':tt_feats[:, 0],
        'Current':tt_feats[:, 1],
        'pH Elapsed':tt_feats[:, 2] ,
        'Temperature':tt_feats[:, 3],
        'Rinse':tt_feats[:, 4],
        'Integrals':tt_feats[:, 5]
    }
    return DataFrame(dict)

def get_model_folder_name():
    return "gold_fc_prod"

def get_table_name():
    return 'gold_fc'

def get_std_params_table_name():
    return 'std_params_gold'

def get_data_folder_name():
    return "Data"

def get_num_folds():
    return 4

def predict_ppm(model, features):
    return model.predict(features)

def load_from_cloud():

    # Specify the public ID or the URL of the ZIP file to download
    zip_public_id = f'{get_model_folder_name()}.zip'  # Or provide the URL of the ZIP file
    # Get the download URL for the ZIP file from Cloudinary
    download_url = cloudinary.utils.cloudinary_url(zip_public_id,
                                                   resource_type='raw')[0]

    response = requests.get(download_url, stream=True)

    save_path = f".\\{zip_public_id}"

    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)

    #Unzip file
    path = os.path.join(os.environ['HOME'], file_management.get_file_path())
    #shutil.unpack_archive(save_path, path)

    return  response
