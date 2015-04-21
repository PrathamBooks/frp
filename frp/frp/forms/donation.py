# -*- coding: utf-8 -*-

import wtforms
import coaster
from .. import app
from .signup import (STATES)

AMOUNT_CHOICES = [(1000, u'Rs. 1000'), 
                  (500, u'Rs. 500'),
                  (250, u'Rs. 250')]

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
    city = wtforms.TextField(
            label='City',
            validators=[wtforms.validators.Optional()])
    state = wtforms.SelectField(
        label='Please select any one state in the list',
        choices=STATES)
    pin = wtforms.TextField(
            label='Pin Code',
            validators=[wtforms.validators.Optional()])
    contact_number = wtforms.TextField(
            label='Contact Number',
            validators=[wtforms.validators.Optional()])
    pan_number = wtforms.TextField(
            label='Contact Number',
            validators=[wtforms.validators.Optional()])
    tax_exemption_certificate = wtforms.RadioField(
        label='Would you like us to send you a Tax Exemption Certificate?',
        coerce=bool,
        default=True,
        choices=[(True, 'Yes'),
                 (False, 'No')])
    ann_choice = wtforms.RadioField(
        label='Would you like to be anonymous?',
        coerce=bool,
        default=False,
        choices=[(True, 'Yes'),
                 (False, 'No')])

    def set_data(self, user):
       self.first_name.data = user.first_name
       self.last_name.data = user.last_name
       self.state.data = user.state
       self.city.data = user.city
       self.pin.data = user.pin
       self.contact_number.data = user.contact_number
       self.pan_number.data = user.pan_number
