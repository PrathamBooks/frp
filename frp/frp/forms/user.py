# -*- coding: utf-8 -*-

from flask import g

import wtforms

from ..models import User
from .signup import STATES

class ProfileForm(wtforms.Form):
    first_name = wtforms.TextField(
        label='First Name', validators=[wtforms.validators.Required('Enter first name'),
                                        wtforms.validators.Length(max=160)])
    last_name = wtforms.TextField(
        label='Last Name', validators=[wtforms.validators.Required('Enter last name'),
                                       wtforms.validators.Length(max=160)],
        default=u'')
    address = wtforms.TextField(
        label='Address', validators=[wtforms.validators.Optional(),
                                     wtforms.validators.Length(max=500)],
        default=u'')
    city = wtforms.TextField(
        label='City', validators=[wtforms.validators.Optional(),
                                     wtforms.validators.Length(max=500)],
        default=u'')
    state = wtforms.SelectField(
        label='State', choices=STATES)

    pin = wtforms.TextField(
        label='Pin Code', validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=15)],
        default=u'')
    contact_number = wtforms.TextField(
        label='Contact Number', validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=15)],
        default=u'')
    pan_number = wtforms.TextField(
        label='Pan Number', validators=[wtforms.validators.Optional(),
                                        wtforms.validators.Length(max=10)],
        default=u'')
    need_80g_certificate = wtforms.RadioField(
        label='Would you like us to send you a Tax Exemption Certificate?',
        default=False,
        validators=[wtforms.validators.Required()],
        coerce=bool,
        choices=[(True, 'Yes'),
                 (False, 'No')])
 
    def set_data(self, user):
        self.first_name.data = user.first_name
        self.last_name.data = user.last_name
        self.address.data = user.address
        self.city.data = user.city
        self.state.data = user.state
        self.pin.data = user.pin
        self.contact_number.data = user.contact_number
        self.pan_number.data = user.pan_number
        self.need_80g_certificate.data = user.need_80g_certificate
