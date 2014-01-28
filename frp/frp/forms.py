import json

from flask_wtf import Form
from wtforms import TextField, DecimalField, TextAreaField, DateField, FileField, RadioField, ValidationError, BooleanField, Field, SelectMultipleField, SelectField
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

class SearchQueryField(TextField):
    def process_formdata(self, values):
        if values:
            value = values[0]
            print value, type(value)
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
        for val, label, selected in field.iter_choices():
            if selected:
                html.append('<div class="checkbox"><label><input type="checkbox" name="{}[]" value="{}" selected="true"/>{}</label></div>'.format(val, field.name, label))
            else:
                html.append('<div class="checkbox"><label><input type="checkbox" name="{}[]" value="{}"/>{}</label></div>'.format(val, field.name, label))
        return HTMLString(''.join(html))

    # @classmethod
    # def render_option(cls, value, label, selected, **kwargs):
    #     options = dict(kwargs, value=value)
    #     if selected:
    #         options['selected'] = True
    #     return HTMLString('<option %s>%s</option>' % (html_params(**options), escape(text_type(label))))

class CheckBoxSelect(SelectMultipleField):
    widget = CheckBoxSelectWidget()



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

class CampaignForm2(Form):
    category = RadioField('category', choices = [('single_lib', 'Organization/school raising books for a single library'),
                                                 ('multiple_centres', 'You are an organization raising books for multiple centres'),
                                                 ('reading_champ', 'You are a Reading Champion needing books for your sessions'),
                                                 ('behalf', 'Individual raising books on behalf of a school/NGO/others')])
    name = TextField("Name of the Organisation/Individual", validators = [DataRequired()])
    org_status = RadioField('org_status', choices = [("non_profit", "Registered non-profit"),
                                                     ("section_25", "Section 25 Company"),
                                                     ("private_school", "Private School"),
                                                     ("budget_pvt_school", "Budget Private School (fee structure less than Rs.500 per month)"),
                                                     ("govt_school", "Government School"),
                                                     ("library", "Reading centre / library")])
    ho_address = TextField("Head office address")
    ho_phone = TextField("Head office phone number")
    ho_email = TextFieldWithHelp("Info Email ID", help="Please add the organisation info ID. It should not be individual specific.")
    website = TextField("Website")
    fb_page = TextField("Facebook page")
    blog = TextField("Blog Address")

    eightyg_cert = RadioField("80g certification", choices = [("Y","Y"), ("N","N")])

    creator_name = TextField("Your name")
    creator_position = TextField("Position in the organisation")
    creator_email = TextField("Your email address")
    creator_phone = TextField("Your phone number")
    shipping_name = TextField("Name")
    shipping_email = TextField("Shipping email address")
    shipping_phone = TextField("Phone number")

    how_changed = TextAreaField("How it changed the lives of the children you worked with.")

    children_number = TextField("Number of children that you/your organization impacts")
    children_age = TextField("Age group of children you impact")
    
    children_special = CheckBoxSelect("Do you/your organization do any work for following (check all that apply):", 
                                      choices = [("special_needs", "Children with special needs"),
                                                 ("tribal", "Children living in tribal areas"),
                                                 ("xxx", "Children XXX")])

    library = TextField("Books for a a library")
    bookbag = TextField("Books in a bag")
    prize = TextField("Books as a prize")
    reading = TextField("Books for reading sessions")
    language = SelectField("language", choices = [("Hindi","Hindi"),
                                                  ("English","English"),
                                                  ("Marathi","Marathi"),
                                                  ("Telugu","Telugu"),
                                                  ("Gujarati","Gujarati"),
                                                  ("Malayalam","Malayalam")])
    slider1 = TextField("")
    slider2 = TextField("")
    slider3 = TextField("")
    slider4 = TextField("")
    slidertotal = TextField("")



class CategoryForm(Form):
    name = TextField('name', validators = [DataRequired()])
    icon = FileField('icon')

    # campaigns = relationship("Campaign", secondary = category_campaign_table, backref = "categories")

class SearchForm(Form):
    query = SearchQueryField("query")
