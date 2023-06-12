from flask import Flask
from flask import Blueprint, request
import openai


api_key = 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
openai.api_key = api_key

@translate.route('', methods=['POST'])
def post():
    return "post data: " + str(dict(request.values)) + "\n"