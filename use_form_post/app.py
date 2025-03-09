from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app: Flask = Flask(__name__)
login_user_name: str = "osamu"

#Databaseの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

#メッセージのデータベースモデル
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    contents = db.Column(db.String(100))

@app.route("/")
def index():
    #GETメソッドのフォームの値を取得
    search_word: str = request.args.get("search_word")

    #search_word変数の有無を判定
    if search_word is None:
        message_list: list[Message] = Message.query.all()
    else:
        message_list: list[Message] = Message.query.fillter(Message.contents.like(f"%{search_word}%")).all()
    return render_template(
        "top.html",
        login_user_name=login_user_name, 
        message_list=message_list,
        search_word=search_word
        )

@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "GET":
        return render_template("write.html", login_user_name=login_user_name)
    elif request.method == "POST":
        #POSTメソッドのフォーム値を利用して
        #新しいMessageクラスインスタンスを生成する
        contents: str = request.form.get("contents")
        user_name: str = request.form.get("user_name")
        new_message = Message(user_name=user_name, contents=contents)
        db.session.add(new_message)
        #変更をデータベースにコミット
        db.session.commit()
        #message_listに追加してtop.htmlに表示
        return redirect(url_for("index"))
    
#データベースの初期化
with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    app.run(debug=True)