from flask import Flask
from flask import url_for


app = Flask(__name__)


@app.route("/")
def show_index():
	return "index page"


@app.route("/hello")
@app.route("/hello/<name>")
def show_hello(name=None):
	return f"Hello, {name}"



if __name__ == '__main__':
	with app.test_request_context():
		print(url_for("show_index"))
		print(url_for("show_hello"))
		print(url_for("show_hello", name="Taro"))
		
	# app.run(
	# 	host='0.0.0.0', 
	# 	port=5000, # 起動しているサーバ（dockerならコンテナ）のポート番号
	# 	debug=True # デバッグモードをオンにするとインタラクティブに画面を更新することができる
	# )
