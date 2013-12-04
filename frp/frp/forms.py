import json

from flask_wtf import Form
from wtforms import TextField, DecimalField, TextAreaField, DateField, FileField, RadioField, ValidationError, BooleanField, Field
from wtforms.validators import DataRequired, Regexp,  AnyOf
from wtforms.widgets import TextInput
from wtforms import Form as WTFForm


class SearchQueryField(TextField):
    def process_formdata(self, values):
        if values:
            value = values[0]
            print value, type(value)
            try:
                self.data = json.loads(value) # Make sure that it's in JSON
            except ValueError, e:
                raise ValidationError("Sorry. Malformed JSON")
            # Check 'item' key
            if not self.data.has_key("item"):
                raise ValidationError("No 'item' in query.")
            if not self.data['item'] in ['User', 'Campaign', 'Category']:
                raise ValidationError("Can't query on '{}'".format(self.data['item']))
            # Check 'expand' key
            self.data['expand'] = self.data.get('expand', False)
            # The rest should be valid.
        else:
            self.data = ""

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
    latitude = TextField('latitude', validators=[DataRequired()])
    latitude_hem = RadioField(choices=[('N','N'), 
                                       ('S','S')], validators=[DataRequired(), Regexp(r'N|S')])
    longitude = TextField('longitude', validators=[DataRequired()])
    longitude_hem = RadioField(choices=[('E','E'), 
                                        ('W','W')], validators=[DataRequired(), Regexp(r'E|W')])
    start = DatePickerField('start', format='%Y-%m-%d')
    end = DatePickerField('end', format='%Y-%m-%d')
    target =  DecimalField('target', validators = [DataRequired()])


class CategoryForm(Form):
    name = TextField('name', validators = [DataRequired()])
    icon = FileField('icon')

    # campaigns = relationship("Campaign", secondary = category_campaign_table, backref = "categories")

class SearchForm(Form):
    query = SearchQueryField("query")
