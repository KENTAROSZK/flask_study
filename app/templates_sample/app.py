from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route("/")
def index():
	return render_template("top.html")


@app.route("/list")
def item_list():
	return render_template("list.html")


# ページ上で受け取った値を使って画面の要素を変える（動的に切り替える）
@app.route("/detail/<int:id>")
def item_detail(id):
	return render_template("detail.html", show_id=id)


# 複数の値を渡す
@app.route("/multiple")
def show_jinja_multiple():
	word1 = "テンプレートエンジン"
	word2 = "神社"
	return render_template("jinja/show1.html", temp=word1, jinja=word2)


# 辞書で値を渡す
@app.route("/dict")
def show_jinja_dict():
	words = {
		"temp": "テンプレートえんじん",
		"jinja": "ジンジャ"
	}
	return render_template("jinja/show2.html", key=words)


# リストで値を渡す
@app.route("/list2")
def show_jinja_list():
	hero_list = [
		"桃太郎",
		"金太郎",
		"浦島たろう",
	]
	return render_template("jinja/show3.html", users=hero_list)


# -----------------------------------------
# クラスで値を渡す
class Hero:
	def __init__(self, name, age):
		self.name = name
		self.age = age
	# 表示用の関数
	def __str__(self):
		return f"名前{self.name=}, 年齢:{self.age=}"

@app.route("/class")
def show_jinja_class():
	hana = Hero("花咲爺さん", 99)
	return render_template("jinja/show4.html", user=hana)
# -----------------------------------------



# -----------------------------------------
# jinjaの制御構文を試す
class Item:
	def __init__(self, id, name):
		self.id = id
		self.name = name
	def __str__(self):
		return f"商品ID:{self.id=}, 商品名：{self.name=}"

@app.route("/for_list")
def show_for_list():
	item_list = [
		Item(1, "団子"),
		Item(2, "肉まん"),
		Item(9, "doraやき"),
	]
	return render_template("jinja/for_list.html", items=item_list)

@app.route("/if_detail/<int:id>")
def show_if_detail(id):
	item_list = [
		Item(1, "団子"),
		Item(2, "肉まん"),
		Item(9, "doraやき"),
	]
	return render_template("if_detail.html", show_id = id, items=item_list)


@app.route("/if/") # デフォルト値を設定するから、ルートを重ねることができるし、apiで何も受け取っていない時は、デフォルトのリンクでも表示させることができる。この機能必要か？
@app.route("/if/<target>")
def show_jinja_if(target="colourless"):
	print(f"{target=}")
	return render_template("jinja/if_else.html", colour = target)


# -----------------------------------------
# jinjaのフィルター機能を試す

@app.route("/filter")
def show_filter():
	word = "pen"
	return render_template("filter/block.html", show_word=word)

@app.route("/filter2")
def show_filter_variable():
	# クラスを作成
	momo = Hero('桃太郎', 25)
	kinta = Hero('金太郎', 35)
	ura = Hero('浦島タロウ', 45)
	kagu = Hero('かぐや姫', 55)
	kasa = Hero('笠地蔵', 65)
	
	# リストに詰める
	hero_list = [momo, kinta, ura, kagu, kasa]
	return render_template('filter/filter_list.html', heroes = hero_list)


# -----------------------------------------
# jinjaのカスタムフィルターを作成する
@app.template_filter('truncate')
def str_truncate(value, length=10):
	if len(value) > length:
		return value[:length] + "..."
	else:
		return value

@app.route("/filter3")
def show_my_filter():
	word="ジュゲム"
	long_word = 'じゅげむじゅげむごこうのすりきれ'
	return render_template("filter/my_filter.html", show_word1=word, show_word2=long_word)














if __name__ == '__main__':
	app.run(
		host='0.0.0.0', 
		port=5000, # 起動しているサーバ（dockerならコンテナ）のポート番号
		debug=True # デバッグモードをオンにするとインタラクティブに画面を更新することができる
	)
