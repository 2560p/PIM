from flask import Flask

# from routes.transcribe import transcribe_page
# from routes.conversation import conversation_page
# from routes.translate import translate_page
# from routes.tts import tts_page
# from routes.quiz import quiz_page

from lowlevel.lowlevel import ll_endpoint

app = Flask(__name__)

app.register_blueprint(ll_endpoint, url_prefix='/ll')

# app.register_blueprint(transcribe_page, url_prefix='/transcribe')
# app.register_blueprint(conversation_page, url_prefix='/conversation')
# app.register_blueprint(translate_page, url_prefix='/translate')
# app.register_blueprint(tts_page, url_prefix="/tts")
# app.register_blueprint(quiz_page, url_prefix="/quiz")
