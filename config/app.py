from flask import Flask
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    # 'host': 'mongodb://localhost/tiavina-mika-portfolio'
    'host': 'mongodb+srv://tiavinamika:makemehigh@cluster0-j2yxr.mongodb.net/test?retryWrites=true&w=majority'
}