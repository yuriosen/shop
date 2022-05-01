from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FileField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    title = StringField('Наименование товара', validators=[DataRequired()])
    content = TextAreaField("Описание")
    price = StringField("Цена товара (в долларах)")
    photo = FileField("Приложите фото")
    bargaining = BooleanField("Торг возможен?")
    submit = SubmitField('Опубликовать')