from flask_wtf import Form
from wtforms import TextField, DecimalField, TextAreaField, DateField
from wtforms.validators import DataRequired
from wtforms.widgets import TextInput



class DatePickerWidget(TextInput):
    """
    TextInput widget that adds a 'datepicker' class to the html input
    element; this makes it easy to write a jQuery selector that adds a
    UI widget for date picking.
    """
    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'datepicker %s' % c
        return super(DatePickerWidget, self).__call__(field, **kwargs)

class DatePickerField(DateField):
    widget = DatePickerWidget()

class CampaignForm(Form):
    name = TextField('name', validators = [DataRequired()])
    subheading = TextField('subheading')
    brief = TextAreaField('brief')
    description = TextAreaField('description', validators = [DataRequired()])
    start = DatePickerField('start', format='%Y-%m-%d')
    end = DatePickerField('end', format='%Y-%m-%d')
    target =  DecimalField('target', validators = [DataRequired()])


