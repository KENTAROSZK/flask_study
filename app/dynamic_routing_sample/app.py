from flask import Flask
app = Flask(__name__)


def check_type(val):
	print(f"{type(val)=}, {val=}")


@app.route("/dynamic/<value>")
def dynamic_default(value):
	check_type(value)
	return f"<h1>{value=}</h1>"


@app.route("/dynamic2/<int:number>")
def dynamic_converter(number):
	check_type(number)
	return f"<h1>{number=}</h1>"


@app.route("/dynamic3/<value>/<int:number>")
def dynamic_converter_multiple(value, number):
	check_type(value)
	check_type(number)
	return f"<h1>{value=}, {number=}</h1>"


if __name__ == '__main__':
	app.run(
		host='0.0.0.0', 
		port=5000, # 起動しているサーバ（dockerならコンテナ）のポート番号
		debug=True # デバッグモードをオンにするとインタラクティブに画面を更新することができる
	)



