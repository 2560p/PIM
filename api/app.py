from flask import Flask
from lowlevel.lowlevel import ll_endpoint
from main import main_endpoint

app = Flask(__name__)

app.register_blueprint(ll_endpoint, url_prefix='/ll')
app.register_blueprint(main_endpoint, url_prefix='/pim')
