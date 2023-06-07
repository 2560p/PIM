from flask import Flask

from routes.secret import secret_page
from routes.post import post_page

app = Flask(__name__)

app.register_blueprint(secret_page, url_prefix='/secret')
app.register_blueprint(post_page, url_prefix='/post')
