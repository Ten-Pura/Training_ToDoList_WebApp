from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from pymongo import MongoClient
import base64
import os
import hashlib

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/show_picture")
def show_picture():
    return render_template("show_picture.html")

@socketio.on("call picture")
def call_first_picture(index):
    directory = "./picture"
    file_list = [f for f in os.listdir(directory)]
    first_file = os.path.join(directory, file_list[index%len(file_list)])
    with open(first_file, "rb") as f:
        data_byte = f.read()
        data_base64 = base64.b64encode(data_byte).decode('UTF-8')
    emit("read picture", data_base64)

@socketio.on("send img data")
def send_img_data(data_base64):
    #保存するディレクトリを作成
    output_dir = "./picture"
    os.makedirs(output_dir, exist_ok=True)
    #base64データをデコード
    data_byte = base64.b64decode(data_base64.split(",")[1])
    #hash256でファイル名を生成して保存
    hash_object = hashlib.sha256(data_byte)
    file_name = hash_object.hexdigest() + ".png"
    output_path = os.path.join(output_dir, file_name)
    with open(output_path, "wb") as f:
        f.write(data_byte)
    print(f"{file_name}を保存しました。")

if __name__ == "__main__":
    app.run(debug=True)