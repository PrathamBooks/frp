# -*- coding: utf-8 -*-

import wtforms


class LoginForm(wtforms.Form):
    email = wtforms.TextField(
        label='Email', validators=[wtforms.validators.Required(),
                                   wtforms.validators.Email(),
                                   wtforms.validators.Length(max=254)])
    password = wtforms.PasswordField(
        label='Password', validators=[wtforms.validators.Required(),
                                      wtforms.validators.Length(max=80)])
