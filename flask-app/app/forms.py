from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Registrarse')


class SymptomForm(FlaskForm):
    symptoms = TextAreaField('Síntomas', validators=[DataRequired()])
    medication = BooleanField('¿Tomaste algún medicamento?')
    medication_info = StringField('Medicamento (opcional)')
    relief = BooleanField('¿Alivió los síntomas?')
    relief_info = StringField('Detalla el alivio de los sintomas (opcional)')
    submit = SubmitField('Guardar')