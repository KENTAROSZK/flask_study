from flask import Flask, request

app = Flask(__name__)

# ---------------------------
# 5-1
# ルーティング

# GETでデータ取得
@app.route("/get")
def do_get():
	name = request.args.get("name") # リクエストパラメータを取得する
	return f"ハロー、{name}さん"


# POSTでデータ取得
@app.route("/", methods=["GET", "POST"])
def do_get_post():
	if request.method == "POST":
		name = request.form.get("name") # リクエストボディからデータを取得する
		return f"こんにちは、{name}さん"
	return """
	<h2>POSTで送信</h2>
	<form method='post'>
		名前：<input type='text' name='name'>
		<input type='submit' value='送信'>
	</form>
	"""





if __name__ == '__main__':
	app.run(
		host='0.0.0.0', 
		port=5000, # 起動しているサーバ（dockerならコンテナ）のポート番号
		debug=True # デバッグモードをオンにするとインタラクティブに画面を更新することができる
	)