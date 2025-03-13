from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from pymongo import MongoClient
import base64
import gridfs
import bson

app: Flask = Flask(__name__)

socketio = SocketIO(app)

mongo_uri = "mongodb+srv://taichi1166:Ofi33553@cluster0.jslmr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client["SNS"]

#GridFSのセットアップ
fs = gridfs.GridFS(db)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('load messages')
def load_messages():
    messages = db.images.find().sort('_id', -1).limit(3)
    messages = list(messages)[::-1]
    #メッセージと画像データをリストにして返す
    messages_return = [{'message':message['message'],
                        'image_data':get_image_data(message['image_id'])}
                        for message in messages]
    emit("load all messages", messages_return)

def get_image_data(image_id):
    image_file = fs.get(image_id).read()
    image_base64 = base64.b64encode(image_file)
    return image_base64.decode('utf-8')

#メッセージと画像の登録
@socketio.on("send message")
def send_message(data):
    message = data['message']
    image_data = data['image_data']
    image_name = data['image_name']

    #base64エンコードされている画像データをデコードしてGridFSに保存
    image_bytes = base64.b64decode(image_data.split(',')[1])
    image_id = fs.put(image_bytes, image_name=image_name)

    #MongoDBに画像を保存したGridFSのファイルIDとテキストを保存
    image_record = {
        'image_name':image_name,
        'image_id':image_id,
        'message':message
    }
    db.images.insert_one(image_record)

    #メッセージと画像をクライアントへ送信
    emit("load one message", {"message":message, "image_data":get_image_data(image_id)}, broadcast=True)

if __name__ == "__main__":
       socketio.run(app, debug=True)