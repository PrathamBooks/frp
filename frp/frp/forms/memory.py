# -*- coding: utf-8 -*-

import wtforms
import coaster
from .. import app
from .signup import (STATES)

class MemoryForm(wtforms.Form):
    name = wtforms.TextField(
            label='Name',
            validators=[wtforms.validators.Required()])
    city = wtforms.TextField(
            label='City',
            validators=[wtforms.validators.Required()])
    state = wtforms.SelectField(
        label='State',
        choices=STATES)
    email = wtforms.TextField(
            label='Email (will not be displayed)',
            validators=[wtforms.validators.Required()])
    can_share = wtforms.RadioField(
        label='Can we share your book memory to encourage others?',
        default='True',
        choices=[('True', 'Yes'),
                 ('False', 'No')])
    words = wtforms.TextAreaField(
            label='Your Memory',
            validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=500)])
 
