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