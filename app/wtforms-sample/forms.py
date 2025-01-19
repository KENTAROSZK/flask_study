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



