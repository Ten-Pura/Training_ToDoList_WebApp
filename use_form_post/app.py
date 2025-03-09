from datetime import datetime
from flask import Flask, render_template, request

#掲示板の一つ一つのメッセージを示すクラス
class Message:
    #コンストラクター
    def __init__(self, id: str, user_name: str, contents: str):
        self.id = id
        self.user_name = user_name
        self.contents = contents

#グローバル変数の宣言
app: Flask = Flask(__name__)
login_user_name: str = "osamu"
message_list: list[Message] = [
        Message("202400502102310", "osamu", "朝からビールですか！楽しみです。"),
        Message("202400502100223", "noriko", "こちらこそ！次回はABコースで！"),
        Message("202400502092101", "osamu", "昨日はHBコーズ楽しかったです！")
    ]

@app.route("/")
def index():
    #GETメソッドのフォームの値を取得
    search_word: str = request.args.get("search_word")

    #search_word変数の有無を判定
    if search_word is None:
        return render_template("top.html", login_user_name=login_user_name, message_list=message_list)
    else:
        filtered_message_list: list[Message] = [
            message for message in message_list if search_word in message.contents
        ]
        return render_template(
            "top.html",
            login_user_name=login_user_name, 
            message_list=filtered_message_list,
            search_word=search_word
            )

@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "GET":
        return render_template("write.html", login_user_name=login_user_name)
    elif request.method == "POST":
        #POSTメソッドのフォーム値を利用して
        #新しいMessageクラスインスタンスを生成する
        id: str = datetime.now().strftime("%Y%m%d%H%M%S")
        contents: str = request.form.get("contents")
        user_name: str = request.form.get("user_name")
        #message_listに追加してtop.htmlに表示
        if contents:
            message_list.insert(0, Message(id, user_name, contents))
        return render_template("top.html", login_user_name=login_user_name, message_list=message_list)

if __name__ == "__main__":
    app.run(debug=True)