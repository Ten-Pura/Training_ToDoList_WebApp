from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("call all chat channels")
def call_all_chat_channels():
    channel_name = [f"channel_{i}" for i in range(10)]
    channel_url = [f"http://127.0.0.1:5000/channel_{i}" for i in range(10)]
    l = [{"name":name, "url":url } for name, url in zip(channel_name, channel_url)]
    emit("load all chat channnels", l)

if __name__ == "__main__":
    socketio.run(app, debug=True)