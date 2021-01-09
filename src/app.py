import os
from bricklink_api.auth import oauth
from flask import Flask
from flask_cors import CORS
from src.const import *


app = Flask(__name__)
CORS(app)

auth = oauth(
    bricklink_consumer_key,
    bricklink_consumer_secret,
    bricklink_token_value,
    bricklink_token_secret
)

from src.resources import *

app.config['SECRET_KEY'] = os.urandom(12)
