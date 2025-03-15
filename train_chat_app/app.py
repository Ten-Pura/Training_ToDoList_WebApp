from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient

#日本時間（JST）のタイムゾーンを定義
jst = timezone(timedelta(hours=9))

app = Flask(__name__)
socketio = SocketIO(app)

#MongoDBとの接続設定
mongo_uri = "mongodb+srv://taichi1166:Ofi33553@cluster0.jslmr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client    = MongoClient(mongo_uri)
db        = client["chatter_people"]

class Message:
    def __init__(self, record:dict ):
        self.message =  record.get("message")
        self.name    =  record.get("name")
        self.date    =  record.get("date")
        self.channel =  record.get("channel")

    def get_dict(self):
        d = {
            "message" : self.message,
            "name"    : self.name,
            "datetime": self.date,
            "channel" : self.channel
        }
        return d

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/channel/<int:chat_channel>")
def channel_0(chat_channel:int):
    return render_template("chat_channel.html", chat_channel=chat_channel)

@socketio.on("call all chat channels")
def call_all_chat_channels():
    channel_name = [f"channel_{i}" for i in range(10)]
    channel_url = [f"https://verbose-umbrella-674xwq4ww9rhx6q5-5000.app.github.dev/channel/{i}" for i in range(10)]
    l = [{"name":name, "url":url } for name, url in zip(channel_name, channel_url)]
    emit("load all chat channnels", l)

@socketio.on("call all chats")
def call_all_messages(chat_channel):
    print(type(chat_channel))
    print(chat_channel)
    collection = db[chat_channel]
    messages   = collection.find().sort("_id", -1).limit(10)
    messages   = list(messages)[::-1]
    messages   = [{ k : v for k, v in d.items() if k != "_id" } for d in messages]
    emit("load all chats", messages)

@socketio.on("send chat")
def send_chat(record):
    d          = Message(record)
    d.date     = datetime.now(timezone.utc).astimezone(jst).strftime('%Y/%m/%d %H:%M:%S')
    collection = db[str(d.channel)]
    collection.insert_one(d.get_dict())
    emit("load last chat", d.get_dict(), broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)