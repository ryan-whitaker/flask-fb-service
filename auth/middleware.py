from functools import wraps
from flask import request, abort
import os
import json
import jwt

from auth.public_key_extractor import exctract_public_key

SERVICE_ACCOUNT = json.loads(os.getenv('SERVICE_ACCOUNT'))

try:
    public_key = SERVICE_ACCOUNT["public_key"]
except:
    public_key = exctract_public_key(SERVICE_ACCOUNT["private_key"])

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            print("No authorization header!")
            abort(401)
        user = None
        token = request.headers['Authorization'].split(' ')[1]
        try:
            user = jwt.decode(token, public_key, algorithms=['RS256'])
        except:
            print("Unable to decode token!")
            abort(401)

        return f(user, *args, **kws)            
    return decorated_function