from app import app
import flask
from flask import request, send_file
from app import app
from models.upload_model import upload_model
# from models.auth_model import auth_model
import os
from datetime import datetime


# uploadObj = chat_model()
obj = None
file = "abc.txt"
@app.route("/user/<uid>/avatar/upload", methods=["PATCH"])
def upload(uid):
    new_filename = str(datetime.now().timestamp()).replace(".", "")  # Generating unique name for the file
    split_filename = file.filename.split(".")  # Spliting ORIGINAL filename to seperate extenstion
    ext_pos = len(split_filename) - 1  # Canlculating last index of the list got by splitting the filname
    ext = split_filename[ext_pos]  # Using last index to get the file extension
    db_path = f"uploads/{new_filename}.{ext}"
    file.save(f"uploads/{new_filename}.{ext}")
    return obj.upload_avatar_model(uid, db_path)


@app.route("/user/avatar/<uid>", methods=["GET"])
def get_avatar(uid):
    data = obj.get_avatar_path_model(uid)
    root_dir = os.path.dirname(app.instance_path)
    return send_file(f"{root_dir}{data['payload'][0]['avatar']}")
