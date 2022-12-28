from app import app
from flask import request, jsonify

from auth.auth import login, signup, update_profile, update_password, delete
from auth.middleware import authorize

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    auth_payload = request.get_json(force=True)
    user = login(auth_payload["email"], auth_payload["password"])
    return jsonify(user)

@app.route('/signup', methods=['GET', 'POST'])
def signup_route():
    payload = request.get_json(force=True)["body"]
    user = signup(payload)
    return jsonify(user)

@app.route('/settings/profile/delete', methods=['GET', 'POST'])
def delete_route(user):
    payload = {
        "uid": user["user"]["uid"],
        **request.get_json(force=True)["body"]
    }
    user_data = delete(payload)
    return user_data

@app.route('/settings/profile/update', methods=['GET', 'POST'])
@authorize
def update_profile_route(user):
    payload = {
        "user_data": request.get_json(force=True),
        "uid": user["user"]["uid"]
    }
    user_data = update_profile(payload)
    return jsonify(user_data)

@app.route('/settings/email/update', methods=['GET', 'POST'])
@authorize
def update_email_route(user):
    payload = {
        "user_data": request.get_json(force=True),
        "uid": user["user"]["uid"]
    }
    user_data = update_profile(payload)
    return jsonify(user_data)

@app.route('/settings/password/update', methods=['GET', 'POST'])
@authorize
def update_password_route(user):
    payload = {
        **request.get_json(force=True),
        "uid": user["user"]["uid"],
        "email": user["user"]["email"]
    }
    user_data = update_password(payload)
    return jsonify(user_data)