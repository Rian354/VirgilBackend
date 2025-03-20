import sqlite3
from datetime import datetime, timedelta
from flask import make_response, jsonify
import jwt

DB_PATH = "/Users/saurabhatri/Dev/virgil.sqlite"

class user_model:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cur = self.conn.cursor()

    def __del__(self):
        """ Close connection when object is deleted """
        self.conn.close()

    def all_user_model(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        return make_response({"payload": result}, 200) if result else make_response({"message": "No Data Found"}, 204)

    def add_user_model(self, data):
        query = "INSERT INTO users(name, email, password) VALUES(?, ?, ?)"
        self.cur.execute(query, (data['name'], data['email'], data['password']))
        self.conn.commit()
        return make_response({"message": "CREATED_SUCCESSFULLY"}, 201)

    def add_multiple_users_model(self, data):
        query = "INSERT INTO users(name, email, password) VALUES (?, ?, ?)"
        self.cur.executemany(query, [(u['name'], u['email'], u['password']) for u in data])
        self.conn.commit()
        return make_response({"message": "CREATED_SUCCESSFULLY"}, 201)

    def delete_user_model(self, user_id):
        self.cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        return make_response({"message": "DELETED_SUCCESSFULLY"}, 202) if self.cur.rowcount > 0 else make_response({"message": "CONTACT_DEVELOPER"}, 500)

    def update_user_model(self, data):
        query = "UPDATE users SET name = ?, email = ? WHERE id = ?"
        self.cur.execute(query, (data['name'], data['email'], data['id']))
        self.conn.commit()
        return make_response({"message": "UPDATED_SUCCESSFULLY"}, 201) if self.cur.rowcount > 0 else make_response({"message": "NOTHING_TO_UPDATE"}, 204)

    def patch_user_model(self, data):
        query = "UPDATE users SET " + ", ".join([f"{key} = ?" for key in data if key != 'id']) + " WHERE id = ?"
        values = [data[key] for key in data if key != 'id'] + [data['id']]
        self.cur.execute(query, values)
        self.conn.commit()
        return make_response({"message": "UPDATED_SUCCESSFULLY"}, 201) if self.cur.rowcount > 0 else make_response({"message": "NOTHING_TO_UPDATE"}, 204)

    def pagination_model(self, pno, limit):
        pno, limit = int(pno), int(limit)
        start = (pno - 1) * limit
        query = "SELECT * FROM users LIMIT ? OFFSET ?"
        self.cur.execute(query, (limit, start))
        result = self.cur.fetchall()
        return make_response({"page": pno, "per_page": limit, "this_page": len(result), "payload": result}, 200) if result else make_response({"message": "No Data Found"}, 204)

    def user_login_model(self, email, password):
        self.cur.execute("SELECT id, email, firstName, lastName, darkMode FROM users WHERE email = ? AND password = ?", (email, password))
        result = self.cur.fetchall()
        if len(result) == 1:
            exptime = datetime.now() + timedelta(minutes=15)
            data = {"payload": result[0], "exp": int(exptime.timestamp())}
            jwt_token = jwt.encode(data, "Virgil$43413==", algorithm="HS256")
            return make_response({"token": jwt_token, "status": 200}, 200)
        else:
            return make_response({"message": "NO SUCH USER"}, 204)
