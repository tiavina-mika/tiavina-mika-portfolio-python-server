import os
import shutil
from utils.constants import UPLOAD_FOLDER

def save_upload_path(target, filename):
    return '/'.join([target, filename])

def remove_contents(path):
    for c in os.listdir(path):
        full_path = os.path.join(path, c)
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)

def remove_uploaded_file(uploaded_file):
    imagePath = uploaded_file.split('/')
    image = imagePath[len(imagePath) - 1]

    full_path = os.path.join(UPLOAD_FOLDER, image)
    
    if os.path.isfile(full_path):
        os.remove(full_path)