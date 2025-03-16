from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

#Flaskとデータベースの初期化
app:Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///memeo_edit.sqlite"
db:SQLAlchemy = SQLAlchemy(app)

#メモのデータベースモデルを定義
class MemoItem(db.Model):
    id:    int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.Text, nullable=False)
    body:  str = db.Column(db.Text, nullable=False)

#データベースの初期化
with app.app_context():
    db.create_all()

#メモの編集画面を表示する
@app.route("/", methods=["GET", "POST"])
def index():
    items = MemoItem.query.order_by(MemoItem.title).all()
    items.insert(0, {"id":0, "title":"✒️新規作成", "body":""})
    return render_template("list.html", items=items)

@app.route("/memo/<int:id>", methods=["POST", "GET"])
def memo(id: int):
    #メモを取得
    it = MemoItem.query.get(id)
    if it == 0 or it is None:
        #新規メモ
        it = MemoItem(title="__無題__", body="")
    #POSTの場合はデータを保存
    if request.method == "POST":
        it.title = request.form.get("title", "__無題__")
        it.body  = request.form.get("body",  "")
        if it.title == "":
            return "タイトルはからにできません"
        if id == 0:
            db.session.add(it)
        db.session.commit()
        return redirect(url_for("index"))
    #メモの編集画面を表示
    return render_template("memo.html", it=it)

@app.route("/memo/<int:id>/delete")
def delete_memo(id: int):
    it = MemoItem.query.get(id)
    if it is None:
        return "指定したメモは存在しません。"
    db.session.delete(it)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=8888)
