# -*- coding: utf-8 -*-

from flask import g

import wtforms

from ..models import User

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
        self.address.data = user.userinfo.address
        self.contact_number.data = user.userinfo.contact_number
        self.pan_number.data = user.userinfo.pan_number
        self.need_80g_certificate.data = user.userinfo.need_80g_certificate
