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










