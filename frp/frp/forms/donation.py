# -*- coding: utf-8 -*-

import wtforms
import coaster
from .. import app
from .signup import (STATES)

AMOUNT_CHOICES = [(1000, u'Rs. 1000 (28 books)'), 
                  (500, u'Rs. 500 (14 books)'),
                  (250, u'Rs. 250 (7 books)')]
ID_TYPE = [(u'P', u'Passport'),
           (u'DL', u'Driving License'),
           (u'PAN', u'PAN Card'),
           (u'AADHAR', u'Aadhar Card')]

class DonorForm(wtforms.Form):
    amount_choice = wtforms.RadioField(
            label='Donation amount',
            validators=[wtforms.validators.Optional()],
            coerce=int,
            choices=AMOUNT_CHOICES)
    customize_amount = wtforms.IntegerField(
            label='Customize your donation amount',
            validators=[wtforms.validators.Optional(),
                        wtforms.validators.NumberRange(1,10000)])
    first_name = wtforms.TextField(
            label='Name',
            validators=[wtforms.validators.Required()])
    last_name = wtforms.TextField(
            label='Name',
            validators=[wtforms.validators.Optional()])
    address = wtforms.TextField(
        label='Address', validators=[wtforms.validators.Required(),
                                     wtforms.validators.Length(max=500)],
        default=u'')
    city = wtforms.TextField(
            label='City',
            validators=[wtforms.validators.Required()])
    state = wtforms.SelectField(
        label='Please select any one state in the list',
        choices=STATES)
    pin = wtforms.TextField(
            label='Pin Code',
            validators=[wtforms.validators.Required()])
    phone_number = wtforms.TextField(
            label='Phone Number',
            validators=[wtforms.validators.Required()])
    email = wtforms.TextField(
            label='Email',
            validators=[wtforms.validators.Required()])

    identification_type = wtforms.SelectField(
            label='',
            choices=ID_TYPE)
    pan_number = wtforms.TextField(
            label='Pan Number',
            validators=[wtforms.validators.Required()])
    tax_exemption_certificate = wtforms.RadioField(
        label='Would you like us to send you a Tax Exemption Certificate?',
        default='False',
        choices=[('True', 'Yes'),
                 ('False', 'No')])
    ann_choice = wtforms.RadioField(
        label='Would you like to be anonymous?',
        default='False',
        choices=[('True', 'Yes'),
                 ('False', 'No')])

    def set_data(self, user):
       self.first_name.data = user.first_name
       self.last_name.data = user.last_name
       self.state.data = user.state
       self.city.data = user.city
       self.pin.data = user.pin
       self.phone_number.data = user.contact_number
       self.email.data = user.email
       self.pan_number.data = user.pan_number
