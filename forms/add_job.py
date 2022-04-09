from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    product = StringField('Product Title', validators=[DataRequired()])
    price = IntegerField("Price")
    # phone_number = IntegerField("Work Size")
    description = StringField("Description")
    bargaining = BooleanField("Bargaining possible?")
    submit = SubmitField('Submit')
