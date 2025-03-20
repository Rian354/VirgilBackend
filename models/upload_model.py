from flask import make_response, jsonify
import sqlite3

DB_PATH = "/Users/saurabhatri/Dev/virgil.sqlite"


class upload_model:
    def __init__(self):
        """ Initialize database connection and cursor """
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def __del__(self):
        """ Close database connection when object is deleted """
        self.conn.close()

    def upload_file_model(self, uid, db_path):
        """ Update user record with uploaded file path """
        self.cur.execute("UPDATE users SET chatFile=? WHERE id=?", (db_path, uid))
        self.conn.commit()
        if self.cur.rowcount > 0:
            return make_response({"message": "FILE_UPLOADED_SUCCESSFULLY", "path": db_path}, 201)
        else:
            return make_response({"message": "NOTHING_TO_UPDATE"}, 204)

    def get_file_path_model(self, uid):
        """ Retrieve file path for a given user ID """
        self.cur.execute("SELECT chatFile FROM users WHERE id=?", (uid,))
        result = self.cur.fetchone()
        if result:
            return {"payload": dict(result)}  # Convert Row object to dictionary
        else:
            return make_response({"message": "No Data Found"}, 204)
