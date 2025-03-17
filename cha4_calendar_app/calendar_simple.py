import calendar
from flask import Flask, request
from datetime import datetime

#Flaskの初期化
app = Flask(__name__)

#rootにアクセスした時
@app.route("/")
def index():
    year  = int(request.args.get("year",  datetime.now().year))
    month = int(request.args.get("month", datetime.now().month))
    html  = calendar.HTMLCalendar().formatmonth(year, month)
    style = "td {border:1px solid #aaa; width:3em; text-align:center;}"
    return f"<html><body><style>{style}</style>{html}</body></html>"

if __name__ == "__main__":
    app.run(debug=True, port=8888)