from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Наименование товара', validators=[DataRequired()])
    content = TextAreaField("Описание")
    price = IntegerField("Цена товара (в долларах)")
    is_private = BooleanField("Торг возможен?")
    submit = SubmitField('Опубликовать')