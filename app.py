from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

if __name__ == "__main__":
    app.run(port=8000, debug=True)

@app.route("/")
# @auth.token_auth()
def index():
    return jsonify({"Welcome To Virgil": "Guest"})

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

try:
    from controllers import *
except Exception as e:
    print(e)
