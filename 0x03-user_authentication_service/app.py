#!/usr/bin/env python3
"""User authenticated app
"""
from auth import Auth
from flask import Flask, jsonify, request


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
            return jsonify({"email": f"{user.email}", "message": "user created"})
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
