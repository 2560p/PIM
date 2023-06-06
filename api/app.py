from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello, world!"


@app.route('/param/<custom>')
def param(custom):
    return "your submitted parameter is " + custom

@app.route('/query')
def return_data():
    args = request.args
    return "you have submitted this query: " + str(dict(args))
