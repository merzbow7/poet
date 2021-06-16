from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import Email, Length, DataRequired, EqualTo


class AddCommentForm(FlaskForm):
    comment = TextAreaField("Комментарий:", validators=[DataRequired()])
    button = SubmitField("Добавить")


class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[Email(message="Это не email")])
    password = PasswordField("Password:",
                             validators=[DataRequired(), Length(min=4, max=24,
                                                                message='Пароль должен быть от 4 до 25 символов')],
                             )
    remember = BooleanField("Запомнить", default=False)
    next = StringField("", )
    submit = SubmitField("Вход")


class RegisterForm(FlaskForm):
    email = StringField("Email:", validators=[Email(message="Это не email")])
    password = PasswordField("Password:",
                             validators=[DataRequired(), Length(min=4, max=24,
                                                                message='Пароль должен быть от 4 до 25 символов')],
                             )
    password_repeat = PasswordField("Password:",
                                    validators=[EqualTo('password',
                                                        message='Пароли должны совпадать')], )
    button = SubmitField("Регистрация")
