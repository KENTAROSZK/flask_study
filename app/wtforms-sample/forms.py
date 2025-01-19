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





