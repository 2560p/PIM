from flask import Flask

from routes.stt import stt_page
from routes.conversation import conversation_page
from routes.translate import translate_page
from routes.tts import tts_page

app = Flask(__name__)

app.register_blueprint(stt_page, url_prefix='/stt')
app.register_blueprint(conversation_page, url_prefix='/conversation')
app.register_blueprint(translate_page, url_prefix='/translate')
app.register_blueprint(tts_page, url_prefix="/tts")
