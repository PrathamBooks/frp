# -*- coding: utf-8 -*-

import wtforms
from ..models import (
    ORG_STATUS_CHOICES, )

from wtforms import widgets


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


STATES = [
    ('{}'.format(index), state) for index, state in enumerate(
        [
            'Andhra Pradesh', 'Arunachal Pradesh', 'Assam',
            'Bihar', 'Chhattisgarh', 'Delhi', 'Goa', 'Gujarat',
            'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir',
            'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
            'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
            'Nagaland', 'Orissa', 'Punjab', 'Rajasthan', 'Sikkim',
            'Tamil Nadu', 'Tripura', 'UNION TERRITORY', 'Uttar Pradesh',
            'Uttaranchal', 'West Bengal'
        ]
    )
]


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
        label='facebook_page', validators=[wtforms.validators.Optional(),
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

    org_intro = wtforms.TextField(
        label='Please explain briefly the impact that your organisation\'s work is having on children / community it is serving .',
        validators=[wtforms.validators.Required(),
                    wtforms.validators.Length(max=500)],
        widget=widgets.TextArea()
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


PRODUCT_OFFERING_CHOICES = [
    (1, "Books for library"),
    (2, "Library in a Classroom/Books in a Bag"),
    (3, "Books as Prize/Give-Aways"),
    (4, "Books for reading sessions"),
]
LANGUAGE_CHOICES = [
    ("", "Select any Language"),
    ("Hindi", "Hindi"),
    ("English", "English"),
    ("Marathi", "Marathi"),
    ("Telugu", "Telugu"),
    ("Gujrathi", "Gujrathi"),
    ("Malayalam", "Malayalam")
]


class BeneficarySignupForm2(wtforms.Form):
    product_offerings = wtforms.SelectMultipleField(
        label='Do you/your organization do any work for following (check all that apply)',
        validators=[wtforms.validators.Required()],
        coerce=int,
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        choices=PRODUCT_OFFERING_CHOICES)

    product_offerings1 = wtforms.TextField()
    product_offerings2 = wtforms.TextField()
    product_offerings3 = wtforms.TextField()
    product_offerings4 = wtforms.TextField()

    language1 = wtforms.SelectField(
        validators=[wtforms.validators.Required()],
        choices=LANGUAGE_CHOICES)
    begining_to_read1 = wtforms.IntegerField(
        validators=[wtforms.validators.Optional()])
    learning_to_read1 = wtforms.IntegerField(
        validators=[wtforms.validators.Optional()])
    reading_independently1 = wtforms.IntegerField(
        validators=[wtforms.validators.Optional()])
    reading_proficiently1 = wtforms.IntegerField(
        validators=[wtforms.validators.Optional()])

    language2 = wtforms.SelectField(
        choices=LANGUAGE_CHOICES)
    begining_to_read2 = wtforms.IntegerField(
        validators=[wtforms.validators.Optional()])
    learning_to_read2 = wtforms.IntegerField(
        validators=[wtforms.validators.Optional()])
    reading_independently2 = wtforms.IntegerField(
        validators=[wtforms.validators.Optional()])
    reading_proficiently2 = wtforms.IntegerField(
        validators=[wtforms.validators.Optional()])

    language3 = wtforms.SelectField(
        choices=LANGUAGE_CHOICES)
    begining_to_read3 = wtforms.IntegerField(
        validators=[wtforms.validators.Optional()])
    learning_to_read3 = wtforms.IntegerField(
        validators=[wtforms.validators.Optional()])
    reading_independently3 = wtforms.IntegerField(
        validators=[wtforms.validators.Optional()])
    reading_proficiently3 = wtforms.IntegerField(
        validators=[wtforms.validators.Optional()])

    gross_total = wtforms.IntegerField()

    def validate_product_offerings(self, field):
        for val in field.data:
            num_field = getattr(self, "product_offerings{}".format(val))
            if not num_field.data or not num_field.data.isdigit():
                raise wtforms.validators.ValidationError(
                    "Must enter the number of books for the selected option!")

    def validate_gross_total(self, field):
        num_product_offerings = 0
        if self.product_offerings1.data:
            num_product_offerings = num_product_offerings + int(
                self.product_offerings1.data)
        if self.product_offerings2.data:
            num_product_offerings = num_product_offerings + int(
                self.product_offerings1.data)
        if self.product_offerings3.data:
            num_product_offerings = num_product_offerings + int(
                self.product_offerings1.data)
        if self.product_offerings4.data:
            num_product_offerings = num_product_offerings + int(
                self.product_offerings1.data)

        num_books_across_languages = 0

        if self.begining_to_read1.data:
            num_books_across_languages = num_books_across_languages \
                + self.begining_to_read1.data
        if self.learning_to_read1.data:
            num_books_across_languages = num_books_across_languages \
                + self.learning_to_read1.data
        if self.reading_independently1.data:
            num_books_across_languages = num_books_across_languages \
                + self.reading_independently1.data
        if self.reading_proficiently1.data:
            num_books_across_languages = num_books_across_languages \
                + self.reading_proficiently1.data

        if self.begining_to_read2.data:
            num_books_across_languages = num_books_across_languages \
                + self.begining_to_read2.data
        if self.learning_to_read2.data:
            num_books_across_languages = num_books_across_languages \
                + self.learning_to_read2.data
        if self.reading_independently2.data:
            num_books_across_languages = num_books_across_languages \
                + self.reading_independently2.data
        if self.reading_proficiently2.data:
            num_books_across_languages = num_books_across_languages \
                + self.reading_proficiently2.data

        if self.begining_to_read3.data:
            num_books_across_languages = num_books_across_languages \
                + self.begining_to_read3.data
        if self.learning_to_read3.data:
            num_books_across_languages = num_books_across_languages \
                + self.learning_to_read3.data
        if self.reading_independently3.data:
            num_books_across_languages = num_books_across_languages \
                + self.reading_independently3.data
        if self.reading_proficiently3.data:
            num_books_across_languages = num_books_across_languages \
                + self.reading_proficiently3.data

        if num_books_across_languages != num_product_offerings:
            raise wtforms.validators.ValidationError(
                "The Gross total is not equal to the number of product offerings")


class BeneficarySignupForm3(wtforms.Form):
    image_file = wtforms.FileField()
    video_file = wtforms.FileField()
    state = wtforms.SelectMultipleField(choices=STATES)
    project_title = wtforms.TextField()
    short_description = wtforms.TextField(widget=widgets.TextArea())
    org_intro = wtforms.TextField(widget=widgets.TextArea())
    impact_society = wtforms.TextField(widget=widgets.TextArea())
    funds_utilize = wtforms.TextField(widget=widgets.TextArea())


class BeneficarySignupForm4(wtforms.Form):
    campaign_team = wtforms.TextField()


def get_category_text(category_id):
    for category in BENEFICARY_CATEGORY:
        if category_id == category[0]:
            return category[1]
    return ''


def get_org_status_text(category_id):
    for category in ORG_STATUS_CHOICES:
        if category_id == category[0]:
            return category[1]
    return ''
