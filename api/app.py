import os
from dotenv import load_dotenv

from flask import Flask, request

app = Flask(__name__)
load_dotenv()

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

@app.route('/secret')
def secret():
    secret = os.environ.get('SECRET')
    return "the server secret is " + secret

@app.route('/post', methods=['POST'])
def post():
    return "you have submitted the following data: " + str(dict(request.values)) + "\n"
