from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class StaffLoginForm(FlaskForm):
    pin = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=4, max=15,
               message="Password needs to be between 4 - 15 digits.")])
    submit = SubmitField('Login')
