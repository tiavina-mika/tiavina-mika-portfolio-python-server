from flask import Flask
from flask_cors import CORS
from werkzeug.utils import secure_filename
from utils.constants import PROD_DB_URL, LOCAL_DB_URL

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__, static_folder='../static')
CORS(app)
app.config['MONGODB_SETTINGS'] = {
    # 'host': LOCAL_DB_URL
    'host': PROD_DB_URL
}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER