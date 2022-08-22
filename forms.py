from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email

class SignupForm(FlaskForm):
    fullname = StringField("Nombre Completo", validators=[DataRequired()])
    email = StringField("E-mail", validators =[DataRequired(), Email()])
    ci = IntegerField("Cedula de Identidad", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Registrarme")

class LoginForm(FlaskForm):
    ci = IntegerField("Cedula de Identidad", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Ingresar")