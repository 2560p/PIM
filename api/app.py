from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello, world!"


@app.route('/param/<custom>')
def param(custom):
    return "your submitted parameter is " + custom

