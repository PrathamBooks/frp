# -*- coding: utf-8 -*-

import wtforms
import coaster
from .. import app

from ..models import (is_username_exists, is_email_exists, ORG_STATUS_CHOICES,
                      is_org_email_exists, is_org_name_exists)


__all__ = ['DonorSignupForm', 'BeneficiarySignupForm', 'BENEFICIARY_CATEGORY',
           'ORG_WORK_CHOICES']


class DonorSignupForm(wtforms.Form):
    first_name = wtforms.TextField(
        label='First Name', validators=[wtforms.validators.Required('Enter first name'),
                                        wtforms.validators.Length(max=160)])
    last_name = wtforms.TextField(
        label='Last Name', validators=[wtforms.validators.Required('Enter last name'),
                                       wtforms.validators.Length(max=160)],
        default=u'')
    user_name = wtforms.TextField(
        label='User Name', validators=[wtforms.validators.Required('Enter user name'),
                                       wtforms.validators.Length(max=80)])
    password = wtforms.PasswordField(
        label='Password', validators=[wtforms.validators.Required('Enter password'),
                                      wtforms.validators.Length(max=80)])
    email = wtforms.TextField(
        label='Email', validators=[wtforms.validators.Required('Enter email Id'),
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


BENEFICIARY_CATEGORY = [
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


class BeneficiarySignupForm(wtforms.Form):
    category = wtforms.RadioField(
        label='Which category best describes you? *',
        validators=[wtforms.validators.Required()],
        coerce=int,
        choices=BENEFICIARY_CATEGORY)
    title = wtforms.TextField(
        label='Name of the Organisation/Individual ',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=160)])
    organization_status = wtforms.RadioField(
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
        label='Website', validators=[wtforms.validators.Optional(),
                                     wtforms.validators.URL(),
                                     wtforms.validators.Length(max=500)])
    facebook = wtforms.TextField(
        label='facebook', validators=[wtforms.validators.Optional(),
                                      wtforms.validators.URL(),
                                      wtforms.validators.Length(max=500)])
    blog = wtforms.TextField(
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

    total_impact_on_children = wtforms.IntegerField(
        label='Number of children that you/your organization have impacted since commencement / impacts currently',
        validators=[wtforms.validators.Required()])

    org_work = wtforms.SelectMultipleField(
        label='Do you/your organization do any work for following (check all that apply)',
        validators=[wtforms.validators.Required()],
        coerce=int,
        choices=ORG_WORK_CHOICES)

    project_books = wtforms.IntegerField(
        label='Books / Books as Prize or Give-Aways / For Reading Sessions',
        validators=[wtforms.validators.Optional()])

    project_lib_in_classroom = wtforms.IntegerField(
        label='Library in a Classroom/Books in a Bag',
        validators=[wtforms.validators.Optional()])


    project_title = wtforms.TextField(
        label='Please enter the project title here. This is the first thing your Donor sees and you can also be searched with it.',
        validators=[wtforms.validators.Optional(),
                    wtforms.validators.Length(max=100)])

    project_description = wtforms.TextAreaField(
        label='Brief description of your project for which you are seeking funding.',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=100)])

    project_who_are_you = wtforms.TextAreaField(
            label='Who are you ?',
            validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=100)])

    project_impact = wtforms.TextAreaField(
            label='What work do you do and how does it impact society ?',
            validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=100)])

    fund_utilization = wtforms.TextAreaField(
            label='How will the funds be utilized?',
            validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=100)])

    def set_data(self, org):
       self.category.data = org.info.category
       self.title.data = org.title
       self.email.data = org.info.email
       self.organization_status.data = org.info.status
       self.address.data = org.info.address
       self.contact_number.data = org.info.contact_number
       self.website.data = org.info.website
       self.facebook.data = org.info.facebook
       self.has_80g_certificate.data = org.info.has_80g_certificate
       self.person1_name.data = org.info.person1_name
       self.person1_position.data = org.info.person1_position
       self.person1_email.data = org.info.person1_email
       self.person1_phone.data = org.info.person1_phone

       self.total_impact_on_children.data =  org.info.total_impact_on_children
       org_works = org.works
       org_works_selected = []
       for org_work in org_works:
            org_works_selected.append(org_work.choice_id) 
       self.org_work.data = org_works_selected

    # def validate_name(self, field):
    #     name = field.data.strip()

        # Check username is in db.
     #    if is_org_name_exists(name):
      #       msg = u'{} already exists'.format(name)
       #      raise wtforms.ValidationError(msg)

    # def validate_email(self, field):
     #    email = field.data.strip()
# 
 #        # Check organization email exists
 #        if is_org_email_exists(email):
  #           raise wtforms.ValidationError(u'{} already exists.'.format(email))
