# -*- coding: utf-8 -*-

import inspect
from datetime import date

from . import db, BaseNameMixin, BaseMixin


__all__ = ['ORG_STATUS', 'ORG_STATUS_CHOICES', 'Organization',
           'OrganizationInfo', 'OrganizationWork', 'Campaign',
           'is_org_name_exists', 'is_org_email_exists']


def is_org_name_exists(name):
    """Check the username exists in db.

    :param name `unicode`: name to check in db.
    """
    return Organization.query.filter_by(name=name).first()


def is_org_email_exists(email):
    """Check the email exists in db.

    :param email `unicode`: org info email to check in db.
    """
    return OrganizationInfo.query.filter_by(email=email).first()


def get_attrs(cls):
    attrs = inspect.getmembers(cls, lambda a: not(inspect.isroutine(a)))
    return [a for a in attrs if not(a[0].startswith('__') and
                                    a[0].endswith('__'))]


class ORG_STATUS:
    registered_non_profit = {'desc': 'Registered non-profit',
                             'value': 1}
    section_25_company = {'desc': 'Section 25 Company',
                          'value': 2}
    private_school = {'desc': 'Private School',
                      'value': 3}
    budget_private_school = {
        'desc': 'Budget Private School (fee structure less than Rs.500 per month)',
        'value': 4}
    government_school = {'desc': 'Government School',
                         'value': 5}
    reading_centre = {'desc': 'Reading centre / library',
                      'value': 6}
    volunteer  = {'desc': 'Reading Champion / Storyteller / Volunteer',
                      'value': 7}


ORG_STATUS_CHOICES = sorted(map(lambda x: (x[1]['value'], x[1]['desc']),
                                get_attrs(ORG_STATUS)))


class Organization(BaseNameMixin, db.Model):
    __tablename__ = 'organization'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    info = db.relationship("OrganizationInfo",
                           backref=db.backref("org"),
                           uselist=False)
    campaigns = db.relationship("Campaign",
                                backref=db.backref("org"))


class OrganizationInfo(BaseMixin, db.Model):
    __tablename__ = 'organization_info'

    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    email = db.Column(db.Unicode(254), unique=True, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(500), nullable=True, default=u'')
    contact_number = db.Column(db.String(15), nullable=True, default=u'')
    website = db.Column(db.Unicode(500), nullable=True, default=u'')
    facebook = db.Column(db.Unicode(500), nullable=True, default=u'')
    blog = db.Column(db.Unicode(500), nullable=True, default=u'')
    has_80g_certificate = db.Column(db.Boolean(), nullable=False)

    person1_name = db.Column(db.Unicode(160), nullable=True, default=u'')
    person1_position = db.Column(db.Unicode(160), nullable=True, default=u'')
    person1_email = db.Column(db.Unicode(254), nullable=True, default=u'')
    person1_phone = db.Column(db.Unicode(15), nullable=True, default=u'')

    person2_name = db.Column(db.Unicode(160), nullable=True, default=u'')
    person2_position = db.Column(db.Unicode(160), nullable=True, default=u'')
    person2_email = db.Column(db.Unicode(254), nullable=True, default=u'')
    person2_phone = db.Column(db.Unicode(15), nullable=True, default=u'')

    intro = db.Column(db.Unicode(10000), nullable=True, default=u'')
    total_impact_on_children = db.Column(db.Integer, nullable=True)
    age_group_of_children = db.Column(db.Unicode(20), nullable=True, default=u'')


class OrganizationWork(BaseMixin, db.Model):
    __tablename__ = 'organization_work'

    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organization = db.relationship("Organization", backref='works')
    choice_id = db.Column(db.Integer, nullable=False)

class Campaign(BaseMixin, db.Model):
    __tablename__ = 'campaign'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nbooks = db.Column(db.Integer(), nullable=True)
    nlic = db.Column(db.Integer(), nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    title = db.Column(db.Unicode(250), nullable=False)
    description = db.Column(db.Unicode(500), nullable=False)
    who = db.Column(db.Unicode(500), nullable=False)
    impact = db.Column(db.Unicode(500), nullable=False)
    utilization = db.Column(db.Unicode(500), nullable=False)

    def days_remaining(self):
        rdays = 30 - (date.today() - self.created_at.date()).days
        return rdays if rdays > 0 else 0

    def target(self):
        return 50 * (self.nbooks + 125 * self.nlic)
