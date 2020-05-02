from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['MONGODB_SETTINGS'] = {
    # 'host': 'mongodb://localhost/tiavina-mika-portfolio'
    'host': 'mongodb+srv://tiavinamika:makemehigh@cluster0-j2yxr.mongodb.net/test?retryWrites=true&w=majority'
}