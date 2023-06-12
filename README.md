# AI PIM

A helpful AI teacher, assistant, and Dutch language expert

## Branch (folder) structure
- `dev-api` (`/api/`) - contains root of API
- `dev-pico` (`/pico/`) - contains file(-s) for Raspberry Pi Pico

## Workflow
The software team of the group is working on different parts at the same time.

The branches are named in a convention `dev-{specific part}` or `dev-{specific part}-{specific feature}`. At the end of each day, the merge has to be done. Feature sub-branches are merged into their parent branches, which are then merged to `dev`. It is important that every merge conflict is resolved in the features' and parts' branches, and not the dev one.

## API
API responds with JSON formatted data. As of now, a user can get two possible responses:
* `{'success': true, 'data': ...}` - when the request was successful
* `{'success': false, 'error': ...}` - when the request was unsuccessful

When the request was unsuccessful, the response code is either any of 4xx or 5xx. Thus, the client can understand whether the error was on the client or server side. The response will also contain `error` field, which will contain a string with the error message.
