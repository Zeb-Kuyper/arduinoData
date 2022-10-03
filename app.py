from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "<p>Hello, world!</p>"

@app.route('/mary')
def hello_mary():
    return "<p>Hello, Mary!</p>"

@app.route('/john')
def hello_john():
    return "<p>Hello, John!</p>"
