# AI PIM

A helpful AI teacher, assistant, and Dutch language expert

## Folder structure
* `/api/` - contains root of API
* `/pico/` - contains file(-s) for Raspberry Pi Pico

## API
API responds with JSON formatted data. As of now, a user can get two possible responses:
* `{'success': true, 'data': ...}` - when the request was successful
* `{'success': false, 'error': ...}` - when the request was unsuccessful

When the request was unsuccessful, the response code is either any of 4xx or 5xx. Thus, the client can understand whether the error was on the client or server side. The response will also contain `error` field, which will contain a string with the error message.
