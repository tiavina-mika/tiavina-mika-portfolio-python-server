from flask import Flask
from config.db import initialize_db
from config.app import app
import controllers.project

initialize_db(app)