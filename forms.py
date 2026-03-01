from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, EqualTo

class PiezaForm(FlaskForm):
    nombre = StringField('Nombre de la pieza', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[DataRequired()])
    precio = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    categoria = SelectField('Categoría', choices=[
        ('Motor', 'Motor'),
        ('Carrocería', 'Carrocería'),
        ('Frenos', 'Frenos'),
        ('Suspensión', 'Suspensión'),
        ('Transmisión', 'Transmisión'),
        ('Eléctrico', 'Eléctrico')
    ], validators=[DataRequired()])
    submit = SubmitField('Guardar')

class RegistroForm(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirmar = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')