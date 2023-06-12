from flask import Flask

from routes.secret import secret_page
from routes.post import post_page
from routes.test import test_page
from routes.stt import stt_page
from routes.conversation import conversation_page
from routes.translate import translate_page

app = Flask(__name__)

app.register_blueprint(secret_page, url_prefix='/secret')
app.register_blueprint(post_page, url_prefix='/post')
app.register_blueprint(test_page, url_prefix='/test')
app.register_blueprint(stt_page, url_prefix='/stt')
app.register_blueprint(conversation_page, url_prefix='/conversation')
app.register_blueprint(translate_page, url_prefix='/translate')
