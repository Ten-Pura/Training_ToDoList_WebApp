from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("call text")
def read_text():
    text = f"これはテストです。関数{__name__}を読み込んでいます。"
    emit("read text", text)

if __name__ == "__main__":
    app.run(debug=True)