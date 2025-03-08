from flask import Flask

#インスタンスの作成
app: Flask = Flask(__name__)

#ルーティング
@app.route("/")
def hello_world():
    age: int = 19
    return "<h1>あなたの年齢は" + str(age) + "歳です。</h1>"

#アプリの実行
if __name__ == "__main__":
    app.run(debug=True)