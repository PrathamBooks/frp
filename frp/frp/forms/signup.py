# -*- coding: utf-8 -*-

import wtforms
import coaster

from ..models import is_username_exists, is_email_exists, ORG_STATUS_CHOICES


__all__ = ['DonorSignupForm', 'BeneficarySignupForm']


class DonorSignupForm(wtforms.Form):
    first_name = wtforms.TextField(
        label='First Name', validators=[wtforms.validators.Required(),
                                        wtforms.validators.Length(max=160)])
    last_name = wtforms.TextField(
        label='Last Name', validators=[wtforms.validators.Optional(),
                                       wtforms.validators.Length(max=160)],
        default=u'')
    user_name = wtforms.TextField(
        label='User Name', validators=[wtforms.validators.Required(),
                                       wtforms.validators.Length(max=80)])
    password = wtforms.PasswordField(
        label='Password', validators=[wtforms.validators.Required(),
                                      wtforms.validators.Length(max=80)])
    email = wtforms.TextField(
        label='Email', validators=[wtforms.validators.Required(),
                                   wtforms.validators.Email(),
                                   wtforms.validators.Length(max=254)])
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

    def validate_user_name(self, field):
        username = field.data.strip()

        # Check if the username is valid
        if not coaster.valid_username(username):
            raise wtforms.ValidationError('Invalid username.')

        # Check username is in db.
        if is_username_exists(username):
            msg = u'{} already exists'.format(username)
            raise wtforms.ValidationError(msg)

    def validate_email(self, field):
        email = field.data.strip()

        if is_email_exists(email):
            raise wtforms.ValidationError(u'{} already exists.'.format(email))


BENEFICARY_CATEGORY = [
    (1, 'I am an organization/school raising books for a single library'),
    (2, 'I am an organization raising books for multiple centres'),
    (3, 'I am a Reading Champion needing books for my storytelling sessions'),
    (4, 'I am an Individual raising books on behalf of a school/NGO/others')]


ORG_WORK_CHOICES = [
    (1, 'Children in Rural areas'),
    (2, 'Children in low income Urban area'),
    (3, 'Children living in tribal areas'),
    (4, 'Children with special needs'),
    (5, 'Children who are differently abled')]


class BeneficarySignupForm(wtforms.Form):
    category = wtforms.RadioField(
        label='Which category best describes you? *',
        validators=[wtforms.validators.Required()],
        coerce=int,
        choices=BENEFICARY_CATEGORY)
    name = wtforms.TextField(
        label='Name of the Organisation/Individual ',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=160)])
    orginaztion_status = wtforms.RadioField(
        label='Organisation Status',
        validators=[wtforms.validators.Required()],
        coerce=int,
        choices=ORG_STATUS_CHOICES)
    address = wtforms.TextField(
        label='Head Office Address',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=500)])
    contact_number = wtforms.TextField(
        label='Head Office Phone Number',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=15)])
    email = wtforms.TextField(
        label='Info Email ID',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Email(),
                    wtforms.validators.Length(max=254)])
    website = wtforms.TextField(
        label='Address', validators=[wtforms.validators.Optional(),
                                     wtforms.validators.URL(),
                                     wtforms.validators.Length(max=500)])
    facebook = wtforms.TextField(
        label='facebook', validators=[wtforms.validators.Optional(),
                                      wtforms.validators.URL(),
                                      wtforms.validators.Length(max=500)])
    website = wtforms.TextField(
        label='website', validators=[wtforms.validators.Optional(),
                                     wtforms.validators.URL(),
                                     wtforms.validators.Length(max=500)])
    has_80g_certificate = wtforms.RadioField(
        label='Does your organisation have 80G certification',
        validators=[wtforms.validators.Required()],
        coerce=bool,
        choices=[(True, 'Yes'),
                 (False, 'No')])
    org_intro = wtforms.TextField(
        label='Please explain briefly the impact that your organisation\'s work is having on children / community it is serving .',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=500)]
    )
    total_impact_on_children = wtforms.IntegerField(
        label='Number of children that you/your organization have impacted since commencement / impacts currently',
        validators=[wtforms.validators.Required()])
    age_group_of_children = wtforms.TextField(
        label='Age group of children you impact',
        validators=[wtforms.validators.Optional(),
                    wtforms.validators.Length(max=20)])
    org_work = wtforms.SelectMultipleField(
        label='Do you/your organization do any work for following (check all that apply)',
        validators=[wtforms.validators.Required()],
        coerce=int,
        choices=ORG_WORK_CHOICES)
