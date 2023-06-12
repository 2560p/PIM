from flask import Blueprint
from dotenv import load_dotenv
import os

load_dotenv()

secret_page = Blueprint('secret_page', __name__)

@secret_page.route('/')
def secret():
    return "the secret is " + os.getenv('SECRET')
