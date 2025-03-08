from flask import Flask

app: Flask = Flask(__name__)

@app.route("/")
def index():
    return "<h1>これは掲示板のトップページです。</h1>"

@app.route("/write")
def weite():
    return "<h1>これは掲示板の書き込みページです。</h1>"

@app.route("/edit/<int:message_id>")
def edit(message_id):
    return f"<h1>入力は{type(message_id).__name__}型です。</h1>"

if __name__ == "__main__":
    app.run(debug=True)