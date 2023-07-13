# API
## General information
The responses from the API follow the predefined standards explained here.

The endpoint responses are mainly JSON (one exception - `/ll/tts`). They will always contain the `"success"` boolean field.

If the request was successful (`"success": true`), the response is accompanied with `"data"` field. The content of it is explained below.

__Exception!__ `/ll/tts` will respond with an mp3 file when the request is successful.

If the request failed (`"success": false`), the reponse code is either _400_ or _500_.

Error code _500_ means that something on the server side failed, and the request cannot be processed futher.

_400_, on the other hand, means that the user has failed to provide the right request parameter. The response will then contain `"errors"` field, stating what has gone wrong.

## Response breakdown

| Endpoint | Parameters | Response |
| -------- | -------- | -------- |
|/pim | {<br>"audio": _base64 encoded audio_,<br>"mode": _optional, mode of PIM [conversation, translation]_,<br>} | "data": <br>_{<br>"data": message from PIM,<br>"audio": base64 encoded audio of PIM's response <br>}_ <br>**or**<br> _{<br>"mode_switch": {"mode": [conversation, translation]}<br>}_ |
||||
| /ll/transcribe | _file as post data_ | "data": _transcribed text_ |
| /ll/tts | {<br>"lang": _target language (en)_,<br>"text": _text to translate_,<br>} | _mp3 file_ |
| /ll/translate | {<br>&#9;"text": _text to translate_,<br>} | "data": _translated text_ |
| /ll/conversation | {<br>"message": _message_<br>} | "data": _reply to the message_ |
| /ll/quiz | {<br>"level": _level of complexity (initial, beginner, intermediate, advanced)_<br>} | "data": _[{"question": "__word in Dutch__", "answer": "__word in English__"}, ... (10 questions in total)]_
