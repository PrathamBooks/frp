# -*- coding: utf-8 -*-

import wtforms
import coaster
from .. import app

from ..models import (is_email_exists, ORG_STATUS_CHOICES,
                      is_org_email_exists, is_org_name_exists)


__all__ = ['BeneficiarySignupForm', 'BENEFICIARY_CATEGORY',
           'ORG_WORK_CHOICES', 'LANGUAGE_CHOICES', 'STATES']


BENEFICIARY_CATEGORY = [
    (1, 'I am an Organisation/School raising funds for books for a single library'),
    (2, 'I am an Organisation raising funds for books for multiple centers'),
    (3, 'I am a Reading Champion raising funds for books for my storytelling sessions'),
    (4, 'I am an Individual raising funds for books on behalf of a School/NGO/Others')]


ORG_WORK_CHOICES = [
    (1, 'Children in rural areas'),
    (2, 'Children in low income urban areas'),
    (3, 'Children living in tribal areas'),
    (4, 'Children with special needs'),
    (5, 'Children who are differently-abled')]

LANGUAGE_CHOICES = [
    ('', 'Select'),
    ('English', 'English'),
    ('Hindi', 'Hindi'),
    ('Marathi', 'Marathi'),
    ('Kannada', 'Kannada'),
    ('Telugu', 'Telugu'),
    ('Urdu', 'Urdu')]

STATES = [
        (u'Andhra Pradesh', u'Andhra Pradesh'),
        (u'Arunachal Pradesh', u'Arunachal Pradesh'),
        ("Assam", "Assam"),
        ("Bihar", "Bihar"),
        ("Chhattisgarh", "Chhattisgarh"),
        ("Delhi", "Delhi"),
        ("Goa", "Goa"),
        ("Gujarat", "Gujarat"),
        ("Haryana", "Haryana"),
        ("Himachal Pradesh", "Himachal Pradesh"),
        (u'Jammu and Kashmir', u'Jammu and Kashmir'),
        ("Jharkhand", 'Jharkhand'),
        ("Karnataka", "Karnataka"),
        ("Kerala", "Kerala"),
        (u'Madhya Pradesh', u'Madhya Pradesh'),
        ("Maharashtra", "Maharashtra"),
        ("Manipur", "Manipur"),
        ("Meghalaya", "Meghalaya"),
        ("Mizoram", "Mizoram"),
        ("Nagaland", "Nagaland"),
        ("Orissa", "Orissa"),
        ("Punjab", "Punjab"),
        ("Rajasthan", "Rajasthan"),
        ("Sikkim", "Sikkim"),
        ("Tamilnadu", "Tamilnadu"),
        ("Tripura", "Tripura"),
        (u'Uttar Pradesh', u'Uttar Pradesh'),
        ("Uttaranchal", "Uttaranchal"),
        (u'West Bengal', u'West Bengal')]


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
        description='In case of an individual, a residence address can be given.',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=500)])
    contact_number = wtforms.TextField(
        label='Head Office Phone Number',
        description='In case of an individual, a personal phone number can be given.',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=15)])
    email = wtforms.TextField(
        label='Email ID',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Email(),
                    wtforms.validators.Length(max=254)])
    website = wtforms.TextField(
            label='Website URL', description=u'Website should start with http://',
            validators=[wtforms.validators.Optional(),
                wtforms.validators.URL(),
                wtforms.validators.Length(max=500)])
    facebook = wtforms.TextField(
            label='Facebook link', description=u'Facebook link should start with http://',
            validators=[wtforms.validators.Optional(),
                wtforms.validators.URL(),
                wtforms.validators.Length(max=500)])
    blog = wtforms.TextField(
            label='Blog link', description=u'Blog link should start with http://',
            validators=[wtforms.validators.Optional(),
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
        label='Name', validators=[wtforms.validators.Optional(),
                                       wtforms.validators.Length(max=160)])
    person1_position = wtforms.TextField(
        label='Position in the organisation',
        validators=[wtforms.validators.Optional(),
                    wtforms.validators.Length(max=160)])

    person1_email = wtforms.TextField(
        label='Email Id',
        validators=[wtforms.validators.Optional(),
                    wtforms.validators.Email(),
                    wtforms.validators.Length(max=254)])

    person1_phone = wtforms.TextField(
        label='Phone Number',
        validators=[wtforms.validators.Optional(),
                    wtforms.validators.Length(max=15)])

    person2_name = wtforms.TextField(
        label='Your Name', validators=[wtforms.validators.Optional(),
                                       wtforms.validators.Length(max=160)])
    person2_position = wtforms.TextField(
        label='Position in the organisation',
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

    language1 = wtforms.SelectField(
        label='language1',
        choices=LANGUAGE_CHOICES,
        validators=[wtforms.validators.Required()])

    language2 = wtforms.SelectField(
        label='language2',
        choices=LANGUAGE_CHOICES,
        validators=[wtforms.validators.Optional()])

    language3 = wtforms.SelectField(
        label='language3',
        choices=LANGUAGE_CHOICES,
        validators=[wtforms.validators.Optional()])

    total_impact_on_children = wtforms.IntegerField(
        label='Number of children that will be impacted by this campaign',
        validators=[wtforms.validators.Optional()])

    org_work = wtforms.SelectMultipleField(
        label='Do you/your organisation do any work for following (check all that apply)',
        validators=[wtforms.validators.Required()],
        coerce=int,
        choices=ORG_WORK_CHOICES)

    project_books = wtforms.IntegerField(
        label='Books',
        validators=[wtforms.validators.Optional()])

    project_lib_in_classroom = wtforms.IntegerField(
        label='Library-in-a-classroom (LIC)',
        validators=[wtforms.validators.Optional()])

    project_state = wtforms.SelectField(
        label='Please select any one state in the list',
        validators=[wtforms.validators.Required()],
        choices=STATES)

    project_city = wtforms.TextField(
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=100)])

    project_title = wtforms.TextField(
        label='Please enter a title for your campaign here. This is the first thing a donor will see or search while looking for your campaign.',
        validators=[wtforms.validators.Optional(),
                    wtforms.validators.Length(max=500)])

    project_description = wtforms.TextAreaField(
        label='Brief description of the project for which you are raising funds.',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=1000)])

    project_who_are_you = wtforms.TextAreaField(
            label='Who are you?',
            validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=1000)])

    project_impact = wtforms.TextAreaField(
            label='What work do you do and how does it impact society ?',
            validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=1000)])

    fund_utilization = wtforms.TextAreaField(
            label='How will the funds be utilized?',
            validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=1000)])

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
       self.project_description.data = ""

       org_works = org.works
       org_works_selected = []
       for org_work in org_works:
            org_works_selected.append(org_work.choice_id) 
       self.org_work.data = org_works_selected

       def validate_language1(self, field):
           if field.data == 'Select':
             msg = u'Select at least one language'
             raise wtforms.ValidationError(msg)

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
