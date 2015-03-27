# -*- coding: utf-8 -*-

import inspect
import sets
from datetime import date

from . import db, BaseNameMixin, BaseMixin

from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable

__all__ = ['ORG_STATUS', 'ORG_STATUS_CHOICES', 'Organization',
           'OrganizationInfo', 'OrganizationWork', 'Campaign',
           'is_org_name_exists', 'is_org_email_exists']

make_searchable(options={'remove_symbols' : ''})

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
    private_school = {'desc': 'Private School',
                      'value': 2}
    budget_private_school = {
        'desc': 'Budget Private School (fee structure less than Rs.500 per month)',
        'value': 3}
    government_school = {'desc': 'Government School',
                         'value': 4}
    reading_centre = {'desc': 'Reading centre / library',
                      'value': 5}
    volunteer  = {'desc': 'Reading Champion / Storyteller / Volunteer',
                      'value': 6}


ORG_STATUS_CHOICES = sorted(map(lambda x: (x[1]['value'], x[1]['desc']),
                                get_attrs(ORG_STATUS)))


class Organization(BaseMixin, db.Model):
    __tablename__ = 'organization'

    title = db.Column(db.Unicode(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    info = db.relationship("OrganizationInfo",
                           backref=db.backref("org"),
                           uselist=False)
    campaigns = db.relationship("Campaign",
                                backref=db.backref("org"))


class OrganizationInfo(BaseMixin, db.Model):
    __tablename__ = 'organization_info'

    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    email = db.Column(db.Unicode(254), nullable=False)
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

class CampaignQuery(BaseQuery, SearchQueryMixin):
    pass

class Campaign(BaseMixin, db.Model):
    query_class = CampaignQuery
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
    state = db.Column(db.Unicode(500), nullable=False)
    city = db.Column(db.Unicode(500), nullable=False)
    languages = db.Column(db.Unicode(200), nullable=False)
    image = db.Column(db.Unicode(100), nullable=False)
    status = db.Column(db.Unicode(100), nullable=False)
    donations = db.relationship("Donation", backref=db.backref("campaign"))

    search_vector = db.Column(TSVectorType('title', 'description', 
        'who', 'impact', 'utilization', 'state', 'city', 'languages'))

    @staticmethod
    def all_campaigns_data():
        campaigns = Campaign.query.all()
        retval = []
        for campaign in campaigns:
            retval.append(campaign.verbose_fields())
        return retval

    @staticmethod
    def search(search_string):
        campaigns = Campaign.query.search(search_string).all()
        retval = []
        for campaign in campaigns:
            retval.append(campaign.verbose_fields())
        return retval

    def days_remaining(self):
        rdays = 30 - (date.today() - self.created_at.date()).days
        return rdays if rdays > 0 else 0

    def target(self):
        return 50 * (self.nbooks + 125 * self.nlic)

    def total_donations(self):
        return sum(map(lambda x: x.amount, self.donations))

    def percentage_funds_raised(self):
        return int(round((self.total_donations() * 100) /self.target()))
    def verbose_fields(self):
        return {"id" : self.id,
                "title" : self.title,
                "description" : self.description,
                "impact" : self.org.info.total_impact_on_children,
                "languages" : self.languages,
                "type" : ORG_STATUS_CHOICES[self.org.info.status][1],
                "state" : self.state,
                "city" : self.city,
                "target" : self.target(),
                "total_donations" : self.total_donations(),
                "status" : "ACTIVE",
                "nfunders" : len(sets.Set(self.donor_list()))}

    def donor_list(self):
        return map(lambda x: x.user_id, self.donations)

    def is_active(self):
        return ((int (self.days_remaining())) > 0 )



