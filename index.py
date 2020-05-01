from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<h1>Hi there !! Welcome to our first app using Python and Flask</h1>"