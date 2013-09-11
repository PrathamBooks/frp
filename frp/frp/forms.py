from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

class ProductForm(Form):
    name = TextField('name', validators = [DataRequired()])
    description = TextField('description')


