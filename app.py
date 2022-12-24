from flask import Flask
from flask_cors import CORS
import json
import os

import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
load_dotenv()

# Set credentials with service account and initialize app
firebase_credentials = json.loads(os.getenv('SERVICE_ACCOUNT'))
cred = credentials.Certificate(firebase_credentials)
fb_key = firebase_credentials["private_key"]
firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['CORS_ALLOW_HEADERS'] = ['Content-Type', 'Authorization']
CORS(app)

import auth.routes

@app.route('/')
def index():
    return "<h1>Welcome to the Flask-Firebase Service!<h1>"