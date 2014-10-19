# -*- coding: utf-8 -*-

import wtforms
from ..models import (
    ORG_STATUS_CHOICES, is_org_email_exists, is_org_name_exists)


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


class BeneficarySignupForm1(wtforms.Form):
    ##22
    category = wtforms.RadioField(
        label='Which category best describes you? *',
        validators=[wtforms.validators.Required()],
        coerce=int,
        choices=BENEFICARY_CATEGORY)
    organization_name = wtforms.TextField(
        label='Name of the Organisation/Individual ',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=160)])
    organization_status = wtforms.RadioField(
        label='Organisation Status',
        validators=[wtforms.validators.Required()],
        coerce=int,
        choices=ORG_STATUS_CHOICES)
    head_off_address = wtforms.TextField(
        label='Head Office Address',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=500)])
    head_off_phone_number = wtforms.TextField(
        label='Head Office Phone Number',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=15)])
    info_email = wtforms.TextField(
        label='Info Email ID',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Email(),
                    wtforms.validators.Length(max=254)])
    website = wtforms.TextField(
        label='Website', validators=[wtforms.validators.Optional(),
                                     wtforms.validators.URL(),
                                     wtforms.validators.Length(max=500)])
    facebook_page = wtforms.TextField(
        label='facebook', validators=[wtforms.validators.Optional(),
                                      wtforms.validators.URL(),
                                      wtforms.validators.Length(max=500)])
    blog_address = wtforms.TextField(
        label='Blog', validators=[wtforms.validators.Optional(),
                                     wtforms.validators.URL(),
                                     wtforms.validators.Length(max=500)])
    has_80g_certificate = wtforms.RadioField(
        label='Does your organisation have 80G certification',
        validators=[wtforms.validators.Required()],
        coerce=bool,
        default=True,
        choices=[(True, 'Yes'),
                 (False, 'No')])
    person1_name = wtforms.TextField(
        label='Your Name', validators=[wtforms.validators.Optional(),
                                       wtforms.validators.Length(max=160)])
    person1_position = wtforms.TextField(
        label='Position in the organization',
        validators=[wtforms.validators.Optional(),
                    wtforms.validators.Length(max=160)])

    person1_email = wtforms.TextField(
        label='Your Email Id',
        validators=[wtforms.validators.Optional(),
                    wtforms.validators.Email(),
                    wtforms.validators.Length(max=254)])

    person1_phone = wtforms.TextField(
        label='Your Phone no',
        validators=[wtforms.validators.Optional(),
                    wtforms.validators.Length(max=15)])

    person2_name = wtforms.TextField(
        label='Your Name', validators=[wtforms.validators.Optional(),
                                       wtforms.validators.Length(max=160)])
    person2_position = wtforms.TextField(
        label='Position in the organization',
        validators=[wtforms.validators.Optional(),
                    wtforms.validators.Length(max=160)])

    person2_email = wtforms.TextField(
        label='Your Email Id',
        validators=[wtforms.validators.Optional(),
                    wtforms.validators.Email(),
                    wtforms.validators.Length(max=254)])

    person2_phone = wtforms.TextField(
        label='Your Phone no',
        validators=[wtforms.validators.Optional(),
                    wtforms.validators.Length(max=15)])

    from wtforms.widgets import TextArea, CheckboxInput
    org_intro = wtforms.TextField(
        label='Please explain briefly the impact that your organisation\'s work is having on children / community it is serving .',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=500)],
        widget=TextArea()
    )
    total_impact_on_children = wtforms.IntegerField(
        label='Number of children that you/your organization have impacted since commencement / impacts currently',
        validators=[wtforms.validators.Required()])
    age_group_of_children = wtforms.TextField(
        label='Age group of children you impact',
        validators=[wtforms.validators.Optional(),
                    wtforms.validators.Length(max=20)])
    # org_work = wtforms.SelectMultipleField(
    #     label='Do you/your organization do any work for following (check all that apply)',
    #     validators=[wtforms.validators.Required()],
    #     coerce=int,
    #     widget=CheckboxInput(),
    #     choices=ORG_WORK_CHOICES)


class GetStartedBeneficarySignupForm(wtforms.Form):
    pass
