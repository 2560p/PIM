# API
## General information
The responses from the API follow the predefined standards explained here.

The endpoint responses are mainly JSON (one exception - `/tts`). They will always contain the `"success"` boolean field.

If the request was successful (`"success": true`), the response is accompanied with `"data"` field. The content of it is explained below.

__Exception!__ `/tts` will respond with an mp3 file when the request is successful.

If the request failed (`"success": false`), the reponse code is either _400_ or _500_.

Error code _500_ means that something on the server side failed, and the request cannot be processed futher.

_400_, on the other hand, means that the user has failed to provide the right request parameter. The response will then contain `"error"` field, stating what has gone wrong.

## Response breakdown

| Endpoint | Parameters | Response |
| -------- | -------- | -------- |
| /transcribe | _file as post data_ | "data": _transcribed text_ |
| /tts | {<br>"lang": _target language_,<br>"text": _text to translate_,<br>} | _mp3 file_ |
| /translate | {<br>&#9;"text": _text to translate_,<br>} | "data": _translated text_ |
| /conversation | {<br>"text": _message_<br>} | "data": _reply to the message_ |
