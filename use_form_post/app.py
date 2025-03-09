from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

#Flaskインスタンスの生成
app: Flask = Flask(__name__)

#Databaseの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

#ログインマネージャーの設定
app.config['SECRET_KEY'] = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)

#ユーザーモデルの作成
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primmary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(25))

#メッセージのデータベースモデル
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    contents = db.Column(db.String(100))

#ユーザーを読み込むためのコールバック
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#ログインユーザー名を保持する変数
@app.before_request
def set_login_user_name():
    global login_user_name
    login_user_name = current_user.username if current_user.is_authenticated else None

#アカウント登録
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == ["GET"]:
        return render_template("signup.html")
    elif request.method == ["POST"]:
        username = request.form.get("username")
        password = request.form.get("password")
        #ユーザーインスタンスを作成
        user = User(username=username, password=generate_password_hash(password))
        db.session.add()
        db.session.commit()
        return redirect("login")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == ["GET"]:
        return render_template("login.html")
    elif request.method == ["POST"]:
        username = request.form.get("username")
        password = request.form.get("password")
        #Userテーブルからusernameに一致するユーザーを取得する
        user = User.query.filter_by(username=username).first()
        if check_password_hash(password, user.password):
            login_user(user)
            return redirect("/")

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
    
@app.route("/update/<int:message_id>", methods=["GET", "POST"])
def update(message_id: int):
    #メッセージIDから更新対象のメッセージを取得
    message: Message = Message.query.get(message_id)
    
    #更新画面を表示
    if request.method == "GET":
        return render_template("update.html", login_user_name=login_user_name, message=message)

    #更新処理
    elif request.method == "POST":
        message.contents = request.form.get("contents")
        db.session.commit()
        return redirect(url_for("index"))
    
@app.route("/delete/<int:message_id>")
def delete(message_id: int):
    #メッセージIDから削除対象のメッセージを取得
    message: Message = Message.query.get(message_id)
    #メッセージの削除
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for("index"))


#データベースの初期化
with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    app.run(debug=True)