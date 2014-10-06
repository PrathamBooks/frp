# -*- coding: utf-8 -*-

from flask import g

import wtforms

from ..models import User
from .signup import DonorSignupForm


class LoginForm(wtforms.Form):
    email = wtforms.TextField(
        label='Email', validators=[wtforms.validators.Required(),
                                   wtforms.validators.Email(),
                                   wtforms.validators.Length(max=254)])
    password = wtforms.PasswordField(
        label='Password', validators=[wtforms.validators.Required(),
                                      wtforms.validators.Length(max=80)])


class ProfileForm(DonorSignupForm):
    # Right now subclassing solves the typing issue.
    # Later, this may go away.

    def set_data(self, user):
        self.first_name.data = user.userinfo.first_name
        self.last_name.data = user.userinfo.last_name
        self.user_name.data = user.username
        self.address.data = user.userinfo.address
        self.contact_number.data = user.userinfo.contact_number
        self.pan_number.data = user.userinfo.pan_number

    def delete_fields(self, *fields):
        for field in fields:
            delattr(self, field)

    def validate_user_name(self, field):
        username = field.data.strip()

        user = User.query.filter_by(username=username).first()
        if user != g.user:
            return super(ProfileForm, self).validate_user_name(field)
