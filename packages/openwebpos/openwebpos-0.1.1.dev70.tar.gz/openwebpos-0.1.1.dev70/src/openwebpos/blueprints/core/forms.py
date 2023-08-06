from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class DatabaseConfigForm(FlaskForm):
    dialect = SelectField(choices=[('mysql', 'MySQL'),
                                   ('postgresql', 'PostgreSQL')])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password',
                              validators=[DataRequired(), EqualTo('password')])
    host = StringField('Host', validators=[DataRequired()])
    port = StringField('Port', validators=[DataRequired()])
    database = StringField('Database', validators=[DataRequired()])
