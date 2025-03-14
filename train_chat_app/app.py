from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
socketio = SocketIO(app)

messages = [{
    "message": "first message",
    "name": "yokomizo",
    "datetime": datetime.now().strftime('%Y/%m/%d %H:%M:%S')
}]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/channel_0")
def channel_0():
    return render_template("chat_channel.html", chat_channel=0)

@socketio.on("call all chat channels")
def call_all_chat_channels():
    channel_name = [f"channel_{i}" for i in range(10)]
    channel_url = [f"http://127.0.0.1:5000/channel_{i}" for i in range(10)]
    l = [{"name":name, "url":url } for name, url in zip(channel_name, channel_url)]
    emit("load all chat channnels", l)

@socketio.on("call all chats")
def call_all_messages():
    emit("load all chats", messages)

@socketio.on("send chat")
def send_chat(record):
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    d = {
        "message":record["message"],
        "name": record["name"],
        "datetime": time
    }
    messages.append(d)
    emit("load last chat", d)

if __name__ == "__main__":
    socketio.run(app, debug=True)