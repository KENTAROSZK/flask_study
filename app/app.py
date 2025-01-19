from flask import Flask

# インスタンス生成
app = Flask(__name__)


# 「http://localhost:8000/」とルーティング
@app.route("/")
def hello_world():
	return "<h1>hello world ! today </h1>"


if __name__ == '__main__':
    app.run(
    	host='0.0.0.0', 
    	port=5000, # 起動しているサーバ（dockerならコンテナ）のポート番号
    	debug=True # デバッグモードをオンにするとインタラクティブに画面を更新することができる
	)