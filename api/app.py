from flask import Flask
from lowlevel.lowlevel import ll_endpoint

app = Flask(__name__)

app.register_blueprint(ll_endpoint, url_prefix='/ll')
