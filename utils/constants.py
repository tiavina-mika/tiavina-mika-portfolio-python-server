import os
from config.app import app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_FOLDER = os.path.join(os.path.join(BASE_DIR, 'static'))
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, app.config['UPLOAD_FOLDER'])
UPLOAD_PATHNAME = '/static/uploads/'

LOCAL_DB_URL = 'mongodb://localhost/tiavina-mika-portfolio'
PROD_DB_URL = 'mongodb+srv://tiavinamika:makemehigh@cluster0-j2yxr.mongodb.net/test?retryWrites=true&w=majority'

ALLOWED_DOC_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
ALLOWED_IMAGE_EXTENSIONS = {'svg', 'png', 'jpg', 'jpeg'}
