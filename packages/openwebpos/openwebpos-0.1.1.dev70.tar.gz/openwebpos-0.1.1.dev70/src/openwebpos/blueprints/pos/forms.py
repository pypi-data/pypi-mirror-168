from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired


class AddItemToOrderForm(FlaskForm):
    """
    Form to add item to order
    """
    quantity = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add')


class TransactionForm(FlaskForm):
    """
    Form to add transaction to order
    """
    amount = StringField('Amount Tendered', validators=[DataRequired()])
    submit = SubmitField('Add')
