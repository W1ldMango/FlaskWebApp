from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# Create registration form
class AuthorisationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = StringField('password', validators=[DataRequired()],
                           render_kw={"type": "password", "placeholder": "Password"})
    submit = SubmitField('Registration')
