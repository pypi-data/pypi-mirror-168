from flask_wtf import FlaskForm
from wtforms import StringField, FileField, DecimalField, \
    SubmitField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, IPAddress


class MenuForm(FlaskForm):
    """
    Form to add/edit a menu.
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class MenuItemForm(FlaskForm):
    """
    Form to add/edit a menu item.
    """
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PagerForm(FlaskForm):
    """
    Form to change the number of items per page.
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Pager')


class IngredientForm(FlaskForm):
    """
    Form to add/edit an ingredient.
    """
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price')
    submit = SubmitField('Submit')


class PrinterForm(FlaskForm):
    """
    Form to add/edit a printer.
    """
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    ip = StringField('IP Address', validators=[DataRequired()])
    port = IntegerField('Port', validators=[DataRequired()])
    submit = SubmitField('Submit')


class StoreForm(FlaskForm):
    """
    Form to add/edit a store.
    """
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip = StringField('Zip', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    website = StringField('Website')
    logo = FileField('Logo')
    submit = SubmitField('Submit')
