# はじめに

requirements.txtの中身を↓のようにしておくべき。
特に、`Werkzeug==2.3.7`は正誤表に書いてあり、見落とすと沼にはまる（ハマった）。


```text:requirements.txt
flask==2.3.2
wtforms==3.0.1
email-validator==2.0.0.post2
flask-wtf==1.1.1
Werkzeug==2.3.7
```

本章で使っているディレクトリは、

```text
┠form-sample // 5-1
┠wtforms-sample // 5-2
┗flask-wtf-sample // 5-3
```


# Formの基本

Formに入力したデータはサーバに送信されて処理される。
まずは、webアプリ開発に必須知識となる、リクエストの種類から説明する。



## 5-1：HTTPメソッドとは？

- HTTPメソッドとは、webアプリがサーバに対して行うリクエストの種類のこと。
- 主要なHTTPメソッドは、2つ。
	- GETメソッド
		- サーバから情報を**取得**するために使用される。webサーバがリクエストされた情報をブラウザに返す。
	- POSTメソッド
		- サーバにデータを**送信**するために使用される。通常はwebフォームの情報を送信するために使用される。webサーバは受信したデータを処理し、応答を返す。
- 違いは、GETは、URLの末尾にデータを追加して送信する一方で、POSTはHTTPボディにデータを含めて送信する。したがって、データを送る情報サイズに違いがある。GETはURLの末尾にデータを追加して送信するため、データ量に制限がある。一方で、POSTはHTTPボディにデータを含めて送信するため、データサイズに制限がない。


```python

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
```


- Flaskのルーティングでは、HTTPメソッドに応じて、異なる動作をさせられる。
- `methods=["GET", "POST"]` は、Flaskアプリのルーディングで、GETとPOSTの両方に対応することを示している。


### 実行結果（POST）

![実行結果](imgs/スクリーンショット-2025-01-19-151434.png)


### 実行結果（GET）

- 実行させるためには、`http://localhost:8000/get?name=jirou`と入力する必要がある。
- 結果、`ハロー、jirouさん！`と表示される



## 5-2 WTFormsを使おう

- WTFormsとは？
	- Flaskで使用されるフォーム処理ライブラリ
	- このライブラリを使うことで、フォームを簡単に作成でき、かつ入力値の検証やセキュリティ対策を簡単に行える
- インストール方法
	- `pip install wtforms==3.0.1`


### 5-2-2：WTFormsの使用方法

- 下表のフィールドを簡単に作成できる。入力フィールドに適用するバリデーション規則も定義可能。

![フィールド](imgs/152610.png)


#### pythonとhtml作成

![フォルダとファイルの作成](imgs/154131.png)



```python:forms.py
from wtforms import Form
from wtforms.fields import (
    StringField, IntegerField, PasswordField, DateField, 
    RadioField, SelectField, BooleanField, TextAreaField,
    EmailField, SubmitField
)

# ---------------------------
# Formクラス
# ユーザ情報クラス
class UserInfoForm(Form):
	name = StringField("名前: ", render_kw={"placeholder": "例)山田 太郎"})
	age = IntegerField("年齢: ", default=20)
	password = PasswordField("パスワード: ")
	confirm_password = PasswordField("パスワード確認: ")
	email = EmailField("メールアドレス: ")
	birthday = DateField("生年月日: ", format="%Y-%m-%d", render_kw={"placeholder": "yyyy/mm/dd"})
	gender = RadioField(
		"性別: ", choices=[("man", "男性"), ("woman", "女性")],
		default = "man"
	)
	area = SelectField("出身地域: ", choices=[("east", "東日本"), ("west", "西日本")])
	is_married = BooleanField("既婚？: ")
	note = TextAreaField("備考: ")
	submit = SubmitField("送信")
```

```python:app.py
from flask import Flask, render_template, request

app = Flask(__name__)

# ------------------------------
# forms.pyで作成したUserInfoFormを利用する
from forms import UserInfoForm

@app.route('/', methods=['GET','POST'])
def show_enter():
    # フォームの作成
    form = UserInfoForm(request.form)
    # POST
    if request.method == "POST":
        pass
    # GET
    return render_template('enter.html', form=form)



if __name__ == '__main__':
	app.run(
		host='0.0.0.0', 
		port=5000, # 起動しているサーバ（dockerならコンテナ）のポート番号
		debug=True # デバッグモードをオンにするとインタラクティブに画面を更新することができる
	)
```

```html:base.html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8" />
    <title>WTForm</title>
</head>
<body>
    {% block title %} タイトル {% endblock %}
    <hr />
    {% block content %} 内容 {% endblock %}
</body>
</html>
```


```html:enter.html
{% extends "base.html" %}

{% block title %}
    <h1>WTForm：入力</h1>
{% endblock %}

{% block content %}
    <form method="POST">
        {{ form.name.label }}{{ form.name(size=20) }}<br>
        {{ form.age.label }}{{ form.age() }}<br>
        {{ form.password.label }}{{ form.password(size=20) }}<br>
        {{ form.confirm_password.label }}{{ form.confirm_password(size=20) }}<br>
        {{ form.email.label }}{{ form.email(placeholder="xxxx@example.com") }}<br>
        {{ form.birthday.label }}{{ form.birthday() }}<br>
        {{ form.gender.label }}{{ form.gender() }}<br>
        {{ form.area.label }}{{ form.area() }}<br>
        {{ form.is_married.label }}{{ form.is_married() }}<br>
        {{ form.note.label }}{{ form.note(style="height:100px; width:150px")}}<br>
        {{ form.submit() }}
    </form>
{% endblock %}
```

- `enter.html`に記載している、`{{ form.フィールド.label }}`には、forms.pyで定義したラベルが表示される。
- `{{ form.name(size=20) }}`の引数部分は、見た目や動作を調整するためのHTML属性を設定する。※他にも調整するための引数がある（ここでは紹介しない）。


##### 実行結果
![実行結果](imgs/154613.png)


### バリデーションを使ってみる（wtforms.validatorsとは？）

- ユーザが入力したデータが適切な形式であるかどうかを確認する方法である。例えば、メアドが正しい形式で入力されているかどうか、数字フィールドに数字が入力されているかどうか、などのチェックを行える。

![バリデーション一覧](imgs/155012.png)


```python:forms.py
# ---------------------------
# バリデーションを追加する

from wtforms.validators import (
	DataRequired, EqualTo, Length, NumberRange, Email
)

class UserInfoForm(Form):
	name = StringField(
		"名前: ",
		validators=[DataRequired('名前は必須入力です')],
		render_kw={"placeholder": "例)山田 太郎"}
	)

	age = IntegerField(
		"年齢: ",
		validators=[NumberRange(18, 100, '入力範囲は18歳から100歳です')],
		default=20
	)

	password = PasswordField(
		"パスワード: ",
		validators=[Length(1, 10,
                        'パスワードの長さは1文字以上10文字以内です'), 
        EqualTo('confirm_password', 'パスワードが一致しません')]
	)

	confirm_password = PasswordField("パスワード確認: ")
	
	email = EmailField(
		"メールアドレス: ",
		validators=[Email('メールアドレスのフォーマットではありません')]
	)

	birthday = DateField(
		"生年月日: ",
		validators=[DataRequired('生年月日は必須入力です')],
		format="%Y-%m-%d",
		render_kw={"placeholder": "yyyy/mm/dd"}
	)
	
	gender = RadioField(
		"性別: ", choices=[("man", "男性"), ("woman", "女性")],
		default = "man"
	)

	area = SelectField("出身地域: ", choices=[("east", "東日本"), ("west", "西日本")])
	is_married = BooleanField("既婚？: ")
	note = TextAreaField("備考: ")
	submit = SubmitField("送信")
```



- 実行すると、`Exception: Install 'email_validator' for email validation support.`のようなエラーが出る。その場合は、`pip install email-validator`しておく。



app.pyに追記しておく。

```python:app.py
from flask import Flask, render_template, request

app = Flask(__name__)


# ------------------
# バリデーション追加したバージョン

from forms import UserInfoForm
@app.route('/', methods=['GET','POST'])
def show_enter():
    # フォームの作成
    form = UserInfoForm(request.form)
    
    # POSTリクエストかつ、入力内容に問題がない時
    if request.method == "POST" and form.validate(): 
    	return render_template("result.html", form=form)
    return render_template('enter.html', form=form)



if __name__ == '__main__':
	app.run(
		host='0.0.0.0', 
		port=5000, # 起動しているサーバ（dockerならコンテナ）のポート番号
		debug=True # デバッグモードをオンにするとインタラクティブに画面を更新することができる
	)
```

- なんも問題が無ければ、`result.html`が表示される



enter.htmlも書き換える
```html:enter.html
{% extends "base.html" %}

{% block title %}
    <h1>WTForm：入力</h1>
{% endblock %}

{% block content %}
    <!-- ▼▼▼リスト 5-8追加部分▼▼▼ -->
    <div style="color: red;">
        {% if form.errors %}
            <ul>
            === エラーメッセージ ===
            {% for k, v in form.errors.items() %}
                <li>{{k}}:{{v}}</li>
            {% endfor %}
            </ul>
        {% endif %}
    </div>
    <!-- ▲▲▲リスト 5-8追加部分▲▲▲ -->
    <form method="POST">
        {{ form.name.label }}{{ form.name(size=20) }}<br>
        {{ form.age.label }}{{ form.age() }}<br>
        {{ form.password.label }}{{ form.password(size=20) }}<br>
        {{ form.confirm_password.label }}{{ form.confirm_password(size=20) }}<br>
        {{ form.email.label }}{{ form.email(placeholder="xxxx@example.com") }}<br>
        {{ form.birthday.label }}{{ form.birthday() }}<br>
        {{ form.gender.label }}{{ form.gender() }}<br>
        {{ form.area.label }}{{ form.area() }}<br>
        {{ form.is_married.label }}{{ form.is_married() }}<br>
        {{ form.note.label }}{{ form.note(style="height:100px; width:150px")}}<br>
        {{ form.submit() }}
    </form>
{% endblock %}
```

- バリデーションで問題を検知したら、その内容が`form.errors`に格納される。



#### 実行結果

##### インプット（成功ケース）
![このインプット](imgs/161042.png)

##### アウトプット（成功ケース）

![アウトプット](imgs/161128.png)


##### アウトプット（失敗ケース）
パスワードを不一致にしたケース

![失敗ケースアウトプット](imgs/161532.png)




### 5-2-3：テンプレートマクロとは？

- テンプレートエンジンにおいて、特定のタグがや記号を使って定義する再利用可能な「テンプレート」のこと。
- jinja2のテンプレートマクロは、よく使用する表示形式を関数として再利用可能とする。

![テンプレマクロ](imgs/161918.png)


#### ファイルを作成する

```html:_formhelpwers.html
{% macro render_field(field) %}
    <dt>{{ field.label }}
    <dd>{{ field(**kwargs)|safe }}
    {% if field.errors %}
        <ul style="color: red;">
        {% for error in field.errors %}
            <li>{{ error }}</li>
        {% endfor %}
        </ul>
    {% endif %}
    </dd>
{% endmacro %}
```

- 1行目：`render_field`がマクロ名
- マクロの内容：
	- ラベルを使用して、フィールドを表示する。もしエラーがあればそのリストを表示する。


##### enter2.htmlを作成する

```html:enter2.html
{% extends "base.html" %}

{% block title %}
    <h1>WTForm：入力（マクロ使用）</h1>
{% endblock %}

{% block content %}
    <!-- formhelpers.htmlで定義したrender_fieldマクロをインポート -->
    {% from "_formhelpers.html" import render_field %}
    <form method="POST" novalidate>
        {{ render_field(form.name) }}
        {{ render_field(form.age) }}
        {{ render_field(form.password) }}
        {{ render_field(form.confirm_password) }}
        {{ render_field(form.email) }}
        {{ render_field(form.birthday) }}
        {{ render_field(form.gender) }}
        {{ render_field(form.area) }}
        {{ render_field(form.is_married) }}
        {{ render_field(form.note) }}
        {{ form.submit() }}
    </form>
{% endblock %}
```

- `{% from "_formhelpers.html" import render_field %}`でファイル`_formhelpers.html`からマクロ「`render_field`」をimportしている。



##### app.pyの修正

```python:app.py
from flask import Flask, render_template, request

app = Flask(__name__)


# ------------------
# テンプレートマクロを活用した場合

from forms import UserInfoForm
@app.route('/', methods=['GET','POST'])
def show_enter():
    # フォームの作成
    form = UserInfoForm(request.form)
    
    # POSTリクエストかつ、入力内容に問題がない時
    if request.method == "POST" and form.validate(): 
    	return render_template("result.html", form=form)
    return render_template('enter2.html', form=form)


if __name__ == '__main__':
	app.run(
		host='0.0.0.0', 
		port=5000, # 起動しているサーバ（dockerならコンテナ）のポート番号
		debug=True # デバッグモードをオンにするとインタラクティブに画面を更新することができる
	)
```

###### 実行結果

![実行結果](imgs/162842.png)


- バリデーションでエラーを検知したところに赤字でエラー内容を記載できている
	- 名前：空欄のまま送信したので、必須項目であることを明示してくれている
	- パスワード：敢えて異なるパスワードを入力したので、それを明示してくれている


### 5-2-4 カスタムバリデータとは？

WTFormsが用意していないバリデータが必要となる場合もある。バリデータを作成することもできる。


```python:forms.py
from wtforms import Form
from wtforms.fields import (
    StringField, IntegerField, PasswordField, DateField, 
    RadioField, SelectField, BooleanField, TextAreaField,
    EmailField, SubmitField
)


# ---------------------------
# Formクラス
# ユーザ情報クラス
# class UserInfoForm(Form):
# 	name = StringField("名前: ", render_kw={"placeholder": "例)山田 太郎"})
# 	age = IntegerField("年齢: ", default=20)
# 	password = PasswordField("パスワード: ")
# 	confirm_password = PasswordField("パスワード確認: ")
# 	email = EmailField("メールアドレス: ")
# 	birthday = DateField("生年月日: ", format="%Y-%m-%d", render_kw={"placeholder": "yyyy/mm/dd"})
# 	gender = RadioField(
# 		"性別: ", choices=[("man", "男性"), ("woman", "女性")],
# 		default = "man"
# 	)
# 	area = SelectField("出身地域: ", choices=[("east", "東日本"), ("west", "西日本")])
# 	is_married = BooleanField("既婚？: ")
# 	note = TextAreaField("備考: ")
# 	submit = SubmitField("送信")



# ---------------------------
# バリデーションを追加する

from wtforms.validators import (
	DataRequired, EqualTo, Length, NumberRange, Email, ValidationError
)

class UserInfoForm(Form):
	name = StringField(
		"名前: ",
		validators=[DataRequired('名前は必須入力です')],
		render_kw={"placeholder": "例)山田 太郎"}
	)

	age = IntegerField(
		"年齢: ",
		validators=[NumberRange(18, 100, '入力範囲は18歳から100歳です')],
		default=20
	)

	password = PasswordField(
		"パスワード: ",
		validators=[Length(1, 10,
                        'パスワードの長さは1文字以上10文字以内です'), 
        EqualTo('confirm_password', 'パスワードが一致しません')]
	)

	confirm_password = PasswordField("パスワード確認: ")
	
	email = EmailField(
		"メールアドレス: ",
		validators=[Email('メールアドレスのフォーマットではありません')]
	)

	birthday = DateField(
		"生年月日: ",
		validators=[DataRequired('生年月日は必須入力です')],
		format="%Y-%m-%d",
		render_kw={"placeholder": "yyyy/mm/dd"}
	)

	gender = RadioField(
		"性別: ", choices=[("man", "男性"), ("woman", "女性")],
		default = "man"
	)

	area = SelectField("出身地域: ", choices=[("east", "東日本"), ("west", "西日本")])
	is_married = BooleanField("既婚？: ")
	note = TextAreaField("備考: ")
	submit = SubmitField("送信")

	# ▼▼▼ 【リスト5.14】 ▼▼▼ 
    # カスタムバリデータ
    # 英数字と記号が含まれているかチェックする
	def validate_password(self, password):
		if not (any(c.isalpha() for c in password.data) and \
				any(c.isdigit() for c in password.data) and \
				any(c in '!@#$%^&*()' for c in password.data)
			):
			raise ValidationError("パスワードには【英数字と記号：!@#$%^&*()】を含める必要があります")
	# ▲▲▲ 【リスト5.14】 ▲▲▲

```


- 「関数名」を「validate_フィールド名」とすることで、「validatepassword」は、フィールド「password」に対する「カスタムバリデータ」として機能する
	- ちなみに、バリデータの中身は，英数字と記号が含まれているかのチェックをしている

##### 実行結果

![実行結果](imgs/163811.png)



## 5-3：Flask-WTFを使おう

- WTFormsを使うことで、フォームの作成やバリデーションを簡単に作成できた。
- 実はもっと簡単に作成できる方法hがある。
- それが、`Falsk-WTF`

### 5-3-1:インストール

`pip install flask-wtf==1.1.1`


### 5-3-2:Flask-WTFの使用方法

![Falsk-WTFのフォルダ構成](imgs/173545.png)


```python:forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email


class InputForm(FlaskForm):
	name = StringField(
		"名前: ",
		validators = [DataRequired("必須入力")]
	)

	email = EmailField(
		"メアド: ",
		validators = [Email("メアドフォーマットに直して。")]
	)

	submit = SubmitField(
		"送信"
	)
```


```python:app.py
from flask import Flask, render_template, session, redirect, url_for
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

from forms import InputForm

@app.route("/", methods = ["GET", "POST"])
def input():
	form = InputForm()

	# POST
	if form.validate_on_submit():
		session["name"] = form.name.data
		session["email"] = form.email.data
		return redirect(url_for("output"))

	# GET
	if "name" in session:
		form.name.data = session["name"]
	if "email" in session:
		form.email.data = session["email"]
	return render_template("input.html")


@app.route("/output")
def output():
	return render_template("output.html")


if __name__ == '__main__':
	app.run(
		host='0.0.0.0', 
		port=5000, # 起動しているサーバ（dockerならコンテナ）のポート番号
		debug=True # デバッグモードをオンにするとインタラクティブに画面を更新することができる
	)
```

- `app.config["SECRET_KEY"]`はFlaskにおいてアプリのセキュリティに関する重要な設定。
	- セッション情報を暗号化するためのキーなどに使用される。
	- 設定値は自分で任意の文字列を指定できるが、長いランダムな文字列が推奨される。今回は`os.urandom(24)`を利用した。
- Flaskでは、`SECRET_KEY`を設定することで、Flask拡張機能で利用されるセキュリティ機能を使用することができるようになる。
	- 例）
		- セッションの保護
		- CSRF保護
			- CSRF：クロスサイト・リクエスト・フォージェリ。ユーザーの意図しない不正なリクエストを送信させる攻撃手法で、ユーザーがログイン中の状態を悪用する。

**▼アプリケーション上の動作**

```mermaid
flowchart TD
    A[input.htmlの表示] --> B[ユーザがnameとemailを正しく入力する]
    B --> C["送信ボタン"を押す]
    C --> D[POSTされる]
    D --> E[app.pyのform.validate_on_submitがTRUEとなる]
    E --> F[output.htmlが表示される]
```

```html:base.html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8" />
    <title>Flask-WTF</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    {% block title %} タイトル {% endblock %}
    <hr />
    {% block content %} 内容 {% endblock %}
</body>
</html>
```


```html:_formhelpers.html
{% macro render_field(field) %}
    <dt>{{ field.label }}
    <dd>{{ field(**kwargs)|safe }}
    {% if field.errors %}
        <ul style="color: red;">
        {% for error in field.errors %}
            <li>{{ error }}</li>
        {% endfor %}
        </ul>
    {% endif %}
    </dd>
{% endmacro %}
```

```html:input.html
{% extends "base.html" %}

{% block title %}
    <h1>Flask-WTF：入力</h1>
{% endblock %}

{% block content %}
    {% from "_formhelpers.html" import render_field %}
    <form method="POST" novalidate>
        {{ form.csrf_token }}
        {{ render_field(form.name) }}
        {{ render_field(form.email) }}
        <br>
        {{ form.submit() }}
    </form>
{% endblock %}
```


- `{{ form.csrf_token }}`は「CSRFトークン」を生成する。
	- CSRFは、攻撃者が被害者に代わって意図しないアクションを実行するために悪意のあるリクエストを送信する攻撃方法。
	- CSRFトークンはこの攻撃を防ぐために使用する。
	- トークンはランダムな文字列であり、フォーム送信時にサーバからクライアントに送信され、フォームを送信する時に再度サーバに送信される。サーバは送信されたトークンが正しい場合のみにリクエストを受け付ける
	- 攻撃者はトークンを知らないため、攻撃を行えない。


```html:output.html
{% extends "base.html" %}

{% block title %}
    <h1>Flask-WTF：出力</h1>
{% endblock %}

{% block content %}
    <div>
        <ul>
            <li>名前: {{session['name']}}</li>
            <li>メールアドレス: {{session['email']}}</li>
        </ul>
        <p><a href="{{ url_for('input') }}">入力画面に戻る</a></p>
    </div>
{% endblock %}
```



```css:style.css
/* ========== 全体のスタイル ========== */
/* 
    body: ページ全体のスタイルを定義します。
    フォントファミリーをArialとsans-serifに設定し、
    背景色を#f7f7f7（薄い灰色）に設定しています。 
*/
body {
    font-family: Arial, sans-serif;
    background-color: #f7f7f7;
}

/* ========== エラーのスタイル ========== */
/* 
    .field-errors: このクラスセレクタは、エラーメッセージのスタイルを定義します。
    色は赤、マージンとパディングは0に設定されています。 
    パディング: パディングは要素の内側のスペースを指します。
    マージン: マージンは要素の外側のスペースを指します。
*/
.field-errors {
    color: red;
    margin: 0;
    padding: 0;
}
/* 
    .field-errors li: このクラスセレクタは、
    エラーメッセージのリストアイテムのスタイルを定義します。
    リストのスタイルタイプはnoneに設定されています。
    noneに設定することで、リストアイテムのマーカー
    （通常は順序なしリストでの黒い点や順序付きリストでの数字）を非表示にできます。
*/
.field-errors li {
    list-style-type: none;
}

/* ========== ヘッダーのスタイル ========== */
/* 
    h1: h1見出しのスタイルを定義します。
    フォントサイズは2em、テキストは中央揃え、上下のマージンは1emに設定しています。
*/
h1 {
    font-size: 2em;
    text-align: center;
    margin-top: 1em;
    margin-bottom: 1em;
}
/* 
    hr: このセレクタは、水平線のスタイルを定義します。
    上下のマージンは1em、ボーダーはなく、上部に1pxの#ccc（薄い灰色）
    のボーダーに設定しています。
*/
hr {
    margin-top: 1em;
    margin-bottom: 1em;
    border: none;
    border-top: 1px solid #ccc;
}

/* ========== フォームのスタイル ========== */
/* 
    form: このセレクタは、フォームのスタイルを定義します。
    表示はフレックスボックス、方向は縦、アイテムは中央揃えに設定しています。
    ※フレックスボックスは、レスポンシブデザインに特に適している
    　レイアウトモデルです。
*/
form {
    display: flex;
    flex-direction: column;
    align-items: center;
}
/* 
    label: このセレクタは、ラベルのスタイルを定義します。
    表示はブロック、下のマージンは0.5emに設定しています。
*/
label {
    display: block;
    margin-bottom: 0.5em;
}
/* 
    input[type=text], input[type=email]: このセレクタは、
    テキスト入力とメール入力のスタイルを定義します。
    パディングは0.5em、ボーダーラディウスは4px、
    ボーダーは1pxの#ccc、幅は100%に設定されています。
    ※ボーダーラディウス（border-radius）は、CSSプロパティの一つで、
    HTML要素の角を丸くするために使用します。
*/
input[type=text], input[type=email] {
    padding: 0.5em;
    border-radius: 4px;
    border: 1px solid #ccc;
    width: 100%;
}
/* 
    input[type=submit]: このセレクタは、送信ボタンのスタイルを定義します。
    背景色は#4CAF50（緑色）、文字色は白、ボーダーはなし、
    ボーダーラディウスは4px、パディングは0.5emと1em、カーソルはポインタ、
    上のマージンは1emに設定しています。
*/
input[type=submit] {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0.5em 1em;
    cursor: pointer;
    margin-top: 1em;
}
/* 
    input[type=submit]:hover: このセレクタは、
    送信ボタンにマウスがホバーした時のスタイルを定義します。
    背景色が#3e8e41（濃い緑色）に変わります。
*/
input[type=submit]:hover {
    background-color: #3e8e41;
}

/* ========== 出力画面のスタイル ========== */
/* 
    div: このセレクタは、div要素のスタイルを定義します。
    表示はフレックスボックス、方向は縦、アイテムは中央揃えに設定しています。
*/
div {
    display: flex;
    flex-direction: column;
    align-items: center;    
}
/* 
    ul: このセレクタは、順序なしリストのスタイルを定義します。
    リストスタイルはなし、左パディングは0に設定しています。
*/
ul {
    list-style: none;
    padding-left: 0;
}
/* 
    li: このセレクタは、リストアイテムのスタイルを定義します。
    下のマージンは0.5emに設定しています。
*/
li {
    margin-bottom: 0.5em;
}
/* 
    a: このセレクタは、リンクのスタイルを定義します。
    色は#4CAF50（緑色）、テキスト装飾はなしに設定しています。
*/
a {
    color: #4CAF50;
    text-decoration: none;
}
/* 
    a:hover: このセレクタは、リンクにマウスがホバーした時の
    スタイルを定義します。
    テキスト装飾が下線に変わります。
*/
a:hover {
    text-decoration: underline;
}

```

cssの説明は省略（教科書でも省略されている）。


#### 実行結果

![実行結果](imgs/185054.png)

- 見た目もそれっぽくきれいなモノができた
- セッション（`session`）を使うことで、DBを使わずに、ページ間でデータを共有することができる
	- `session`オブジェクトは、辞書型のように使えるため、キーと値のペアでデータの保存、抽出ができる。
- 『PRGパターン』（POST-Redirect-GET）は、フォームデータの二重送信を防ぐ手法。ブラウザ更新ボタンや戻るボタンを押しても、フォームに二重でデータが送信されることを防ぐ。
	- 今回のシンプルな例では、PRGパターンのメリットは見出しづらいが、次章移行のDBへのSQL更新処理系を作成するときなどは、役に立つイメージを持ちやすい。

# PRGパターン

![PRGパターン](imgs/185453.png)

