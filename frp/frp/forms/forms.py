import json

from flask_wtf import Form
from wtforms import TextField, DecimalField, TextAreaField, DateField, FileField, RadioField, ValidationError, BooleanField, Field, SelectMultipleField, SelectField, FileField
from wtforms.validators import DataRequired, Regexp,  AnyOf
from wtforms.widgets import TextInput
from wtforms.widgets.core import HTMLString
from wtforms import Form as WTFForm



class TextFieldWithHelp(TextField):
    def __init__(self, *largs, **kargs):
        if "help" in kargs:
            self.help_text = kargs.pop("help")
        else:
            self.help_text = None
        super(TextFieldWithHelp, self).__init__(*largs, **kargs)

class TextAreaWithHelp(TextAreaField):
    def __init__(self, *largs, **kargs):
        if "help" in kargs:
            self.help_text = kargs.pop("help")
        else:
            self.help_text = None
        super(TextAreaWithHelp, self).__init__(*largs, **kargs)

class SearchQueryField(TextField):
    def process_formdata(self, values):
        if values:
            value = values[0]
            try:
                self.data = json.loads(value) # Make sure that it's in JSON
            except ValueError, e:
                raise ValidationError("Malformed JSON")
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


class CheckBoxSelectWidget(object):
    """
    Renders a select field.

    If `multiple` is True, then the `size` property should be specified on
    rendering to make the field useful.

    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of
    `(value, label, selected)`.
    """
    def __init__(self):
        pass

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = []        
        for val, label, checked in field.iter_choices():
            if checked:
                html.append('<div class="checkbox"><label><input type="checkbox" name="{}" value="{}" checked="true"/>{}</label></div>'.format(field.name, val, label))
            else:
                html.append('<div class="checkbox"><label><input type="checkbox" name="{}" value="{}"/>{}</label></div>'.format(field.name, val, label))
        return HTMLString(''.join(html))

    # @classmethod
    # def render_option(cls, value, label, selected, **kwargs):
    #     options = dict(kwargs, value=value)
    #     if selected:
    #         options['selected'] = True
    #     return HTMLString('<option %s>%s</option>' % (html_params(**options), escape(text_type(label))))

class CheckBoxSelect(SelectMultipleField):
    widget = CheckBoxSelectWidget()

