from flask import Flask
import os

from config.db import initialize_db
from config.app import app
import controllers.project
from utils.constants import UPLOAD_FOLDER, STATIC_FOLDER

# create /static folder if not existed
if not os.path.isdir(STATIC_FOLDER):
    os.mkdir(STATIC_FOLDER)

# create /uploads folder if not existed
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
   
#run the app
initialize_db(app)