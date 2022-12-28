import jwt
import os
import json
import datetime
from flask import abort

import pyrebase
from firebase_admin import firestore, auth
from dotenv import load_dotenv

load_dotenv()
service_account = json.loads(os.getenv('SERVICE_ACCOUNT'))
config = json.loads(os.getenv('CONFIG'))
private_key = service_account["private_key"]

firebase = pyrebase.initialize_app(config)
pb_auth = firebase.auth()

def mint_token(user_data):
    user = {
        "uid": user_data["uid"],
        **user_data,
    }

    expDate = datetime.datetime.now() + datetime.timedelta(hours=12)
    expiresIn = 43200

    payload = {
        "user": user,
        "exp": expDate,
    }

    token = jwt.encode(payload, private_key, algorithm="RS256")

    return {
        "token": token,
        "user": user,
        "expiresIn": expiresIn
    }

def verify_session(email, password):
    try:
        pb_auth.sign_in_with_email_and_password(email, password)
    except:
        abort(401)


def login(email, password):
    try:
        db = firestore.client()
        fb_user = pb_auth.sign_in_with_email_and_password(email, password)
        uid = fb_user["localId"]
        user_data = db.collection(u'users').document(uid).get().to_dict()

        user_data = {
            **user_data,
            "uid": uid
        }

        return mint_token(user_data)
    except:
        abort(400, {"message": "Unable to login, check your username and password and try again."})

def signup(payload):
    try:
        db = firestore.client()
        fb_user = pb_auth.create_user_with_email_and_password(payload["email"], payload["password"])

        uid = fb_user["localId"]

        user_data = {
            "email": payload["email"],
            "firstName": payload["firstName"],
            "lastName": payload["lastName"],
            "preferredName": payload["preferredName"],
            "number": payload["phoneNumber"],
            "premium": False,
            "subscribed": False,
        }

        db.collection(u'users').document(uid).set(user_data)

        user_data = {
            **user_data,
            "uid": uid
        }

        return mint_token(user_data)
    except:
        abort(500, {"message": "Unable to create profile."})

def delete(payload):
    email = payload["email"]
    password = payload["password"]
    verify_session(email, password)
    try:
        db = firestore.client()
        uid = payload["uid"]
        db.collection(u'users').document(uid).delete()
        auth.delete_user(uid)
    except:
        abort(500, {"message": "Unable to delete account."})

def update_profile(payload):
    try: 
        uid = payload["uid"]
        user_data = payload["user_data"]

        db = firestore.client()
        db.collection(u'users').document(uid).update(user_data)
        user_data = db.collection(u'users').document(uid).get().to_dict()

        user_data = {
            **user_data,
            "uid": uid
        }

        return mint_token(user_data)
    except:
        abort(500, {"message": "Unable to update profile"})

def update_password(payload):

    uid = payload["uid"]
    email = payload["email"]
    password = payload["password"]
    new_password = payload["new_password"]
    confirm_password = payload["confirm_password"]

    verify_session(email, password)
    
    if new_password != password:
        if new_password != confirm_password:
            abort(400, {"message": "Passwords must match."})
        else:
            try:
                auth.update_user(
                    uid,
                    password=new_password
                )

                db = firestore.client()
                user_data = db.collection(u'users').document(uid).get().to_dict()

                user_data = {
                    **user_data,
                    "uid": uid
                }

                return mint_token(user_data)

            except:
                abort(500, {"message": "Unable to update password."})
    else:
        abort(400, {"message": "New password must not match current password."})

def update_email(payload):
    uid = payload["uid"]
    email = payload["email"]
    password = payload["password"]
    new_email = payload["new_email"]

    verify_session(email, password)
    try:
        db = firestore.client()
        db.collection(u'users').document(uid).update({"email": new_email})
        user_data = db.collection(u'users').document(uid).get().to_dict()
        auth.update_user(uid, email=new_email)

        user_data = {
            **user_data,
            "uid": uid
        }

        return mint_token(user_data)
    except:
        abort(500, {"message": "Unable to update email."})
