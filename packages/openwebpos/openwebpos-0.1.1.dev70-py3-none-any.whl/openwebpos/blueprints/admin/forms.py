from flask_wtf import FlaskForm
from wtforms import StringField, FileField, DecimalField, \
    SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length


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
    submit = SubmitField('Submit')
