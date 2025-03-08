#render_templateのインポート
from flask import Flask, render_template

app: Flask = Flask(__name__)

@app.route("/")
def index():
    login_user_name: str = "osamu"
    #「top.html」に「login_user_name」を当てはめて表示
    return render_template("top.html", login_user_name=login_user_name)

@app.route("/write")
def write():
    #write.htmlの表示
    return render_template("write.html")

@app.route("/edit/<int:message_id>")
def edit(message_id:int):
    return render_template("edit.html", message_id=message_id)

if __name__ == "__main__":
    app.run(debug=True)