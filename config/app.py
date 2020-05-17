from flask import Flask
from flask_cors import CORS
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
# ALLOWED_DOC_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
# ALLOWED_IMAGE_EXTENSIONS = {'svg', 'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_folder='../static')
CORS(app)
app.config['MONGODB_SETTINGS'] = {
    # 'host': 'mongodb://localhost/tiavina-mika-portfolio'
    'host': 'mongodb+srv://tiavinamika:makemehigh@cluster0-j2yxr.mongodb.net/test?retryWrites=true&w=majority'
}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER