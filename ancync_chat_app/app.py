from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from pymongo import MongoClient

app: Flask = Flask(__name__)

#Socket.ioのセットアップ
socketio = SocketIO(app)

#MongoDBの接続設定
mongo_uri = "mongodb+srv://taichi1166:<db_password>@cluster0.jslmr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client["SNS"]
messages_collection = db["messages"]

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('load messages')
def load_messages():
    messages = messages_collection.find().sort("_id", -1).limit(10)
    messages = list(messages)[::-1]
    messages_return = [message['message'] for message in messages]
    print("動いている＿＿＿＿＿だいだい")
    #メッセージをクライアントへ送信
    emit('load all messages', messages_return)


@socketio.on('send message')
def send_message(message):
    print("Send＿Message動いているその1")
    messages_collection.insert_one({'message': message})
    print("動いている＿その2")
    #メッセージをクライアントへ送信
    emit('load one message', message, broadcast=True)

if __name__ == "__main__":
    #socket.ioサーバーの起動
    socketio.run(app, debug=True)
