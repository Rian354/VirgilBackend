from flask import request, send_file, jsonify
from app import app
from models.user_model import user_model
import os
from datetime import datetime


userObj = user_model()


# authObj = auth_model()

@app.route("/user/all")
# @auth.token_auth()
def all_users():
    return userObj.all_user_model()

@app.route("/login")
# @auth.token_auth()
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    payload = [
        {
            'email': email,
            'id': 1,
            'role': 'admin',
        }
    ]
    return userObj.user_login_model(email, password)

@app.route("/user", methods=["POST"])
def add_user():
    return userObj.add_user_model(request.form)


@app.route("/users", methods=["POST"])
def add_multiple_users():
    return userObj.add_multiple_users_model(request.json)


@app.route("/user/delete/<id>", methods=["DELETE"])
def delete_user(id):
    return userObj.delete_user_model(id)


@app.route("/user/update", methods=["PUT"])
def update_user():
    return userObj.update_user_model(request.form)


@app.route("/user/patch", methods=["PATCH"])
def patch_user():
    return userObj.patch_user_model(request.form)


@app.route("/user/page/<pno>/limit/<limit>", methods=["get"])
def pagination(pno, limit):
    return userObj.pagination_model(pno, limit)


@app.route("/user/login")
def user_login():
    auth_data = request.authorization
    return userObj.user_login_model(auth_data['username'], auth_data['password'])
