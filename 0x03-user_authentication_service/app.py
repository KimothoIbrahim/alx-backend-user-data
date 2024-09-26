#!/usr/bin/env python3
"""User authenticated app
"""
from auth import Auth
from flask import (Flask, jsonify, request, abort,
                   make_response, url_for, redirect)


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """App Home
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """ register users
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)

        if user:
            return jsonify({"email": f"{user.email}",
                           "message": "user created"})
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"])
def login():
    """manage sessions
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        sess = AUTH.create_session(email)
        response = make_response(jsonify({"email": f"{email}",
                                 "message": "logged in"}), 200)
        response.set_cookie('session_id', sess, secure=True, httponly=True)
        response.headers['Content-Type'] = 'application/json'
        return response
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """logout
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect(url_for('index'))
    abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """ get User profile
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": f"{user.email}"}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """reset password
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError as err:
        abort(403)


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """reset password
    """
    email = request.form.get("email")
    new_password = request.form.get("new_password")
    reset_token = request.form.get("reset_token")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError as err:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
