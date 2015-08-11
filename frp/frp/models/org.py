# -*- coding: utf-8 -*-

from __future__ import division
import inspect
import sets
from datetime import *
from flask import current_app

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
    registered_non_profit = {'desc': 'Not-for-Profit Organisation',
                             'value': 1}
    private_school = {'desc': 'Private School',
                      'value': 2}
    budget_private_school = {
        'desc': 'Budget Private School (fee structure less than Rs.500 per month)',
        'value': 3}
    government_school = {'desc': 'Government School',
                         'value': 4}
    reading_centre = {'desc': 'Reading Centre / Library',
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
    description = db.Column(db.Unicode(1500), nullable=False)
    who = db.Column(db.Unicode(3000), nullable=False)
    impact = db.Column(db.Unicode(4000), nullable=False)
    total_impact_on_children = db.Column(db.Integer, nullable=True)
    utilization = db.Column(db.Unicode(4000), nullable=False)
    state = db.Column(db.Unicode(500), nullable=False)
    city = db.Column(db.Unicode(500), nullable=False)
    languages = db.Column(db.Unicode(200), nullable=False)
    image = db.Column(db.Unicode(100), nullable=False)
    status = db.Column(db.Unicode(100), nullable=False)
    featured = db.Column(db.BOOLEAN, nullable=False)
    donations = db.relationship("Donation", backref=db.backref("campaign"))
    comments = db.relationship("Comment", backref=db.backref("campaign_comment"))
    approved_at = db.Column(db.DateTime, nullable=True)

    search_vector = db.Column(TSVectorType('title', 'description', 
        'who', 'impact', 'utilization', 'state', 'city', 'languages'))

    @staticmethod
    def all_campaigns_data(*args):
        campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
        if len(args) == 0:
            retval = map(lambda x:x.verbose_fields(),campaigns)
        else:
            campaigns = filter(lambda x:(x.status in (args)),campaigns)
            retval = map(lambda x:x.verbose_fields(),campaigns)
        return retval

    @staticmethod
    def campaigns_by_date():
        all_campaigns = Campaign.query.order_by(Campaign.created_at).all()
        return map(lambda x : {"year" : x.created_at.date().year, 
                               "month" : x.created_at.date().month, 
                               "day" : x.created_at.date().day}, all_campaigns)


    @staticmethod
    def last_day_today():
        campaigns = Campaign.query.filter_by(status='Approved').all()
        retval = list(filter(lambda x:(x.days_remaining()==0),campaigns))
        return retval

    @staticmethod
    def last_week():
        campaigns = Campaign.query.filter_by(status='Approved').all()
        retval = list(filter(lambda x:(x.days_remaining()==7),campaigns))
        return retval

    @staticmethod
    def search(search_string):
        campaigns = Campaign.query.search(search_string).all()
        args=['Approved', 'Closed']
        campaigns = filter(lambda x:(x.status in (args)), campaigns)
        retval = map(lambda x:x.verbose_fields(),campaigns)
        return retval

    @staticmethod
    def total_books_donated():
        books = map(lambda x: x.books_donated(), Campaign.query.all())
        return reduce(lambda x, y: x + y, books, 0)


    def emails(self):
        mails = [self.created_by.email, self.org.info.email, self.org.info.person1_email]
        mails = filter(lambda x: x, mails)
        mails = list(set(mails))
        return mails


    def approved_date(self):
        if (self.approved_at != None):
            return "{:%B %d, %Y}".format(self.approved_at)
        return "None"

    def approved_date_set(self):
        self.approved_at = datetime.now()


    def days_remaining(self):
        if (self.approved_at != None):
            rdays = 30 - (datetime.now() - self.approved_at).days
            return rdays if rdays > 0 else 0
        return 0

    def start_date(self):
        return self.created_at.date()

    def end_date(self):
        if (self.approved_at != None):
            return self.approved_at + timedelta(days=30)
        else:
            return self.created_at.date() + timedelta(days=30)

    def books_target(self):
        return self.nbooks + 125 * self.nlic

    def cost_per_book(self):
        if (self.start_date() < date(2015, 8, 10)):
            return current_app.config.get('OLD_COST_PER_BOOK')
        else:
            return current_app.config.get('COST_PER_BOOK')

    def target(self):
        return int(round(self.cost_per_book() * (self.nbooks + 125 * self.nlic)))

    def total_donations(self):
        fdonations = filter(lambda x: x.confirmation, self.donations)
        return sum(map(lambda x: x.amount, fdonations))

    def print_status(self):
        if self.status == 'Approved':
            return 'Active'
        else:
            return self.status

    def verbose_fields(self):
        return {"id" : self.id,
                "title" : self.title,
                "org_name": self.org.title,
                "description" : self.description,
                "impact" : self.total_impact_on_children,
                "languages" : self.languages,
                "type" : ORG_STATUS_CHOICES[self.org.info.status - 1][1],
                "state" : self.state,
                "city" : self.city,
                "who"  : self.who,
                "start_date": "{:%B %d, %Y}".format(self.start_date()),
                "end_date" : "{:%B %d, %Y}".format(self.end_date()),
                "days_remaining" : self.days_remaining(),
                "num_donors": self.num_donors(),
                "target" : self.target(),
                "total_donations" : self.total_donations(),
                "status" : self.print_status(),
                "featured" : self.featured,
                "image" : self.image,
                "funds_raised" :self.percent_funded()
                }

    def campaign_details(self):
        return [self.title,
                "{:%B %d, %Y}".format(self.start_date()),
                self.days_remaining(),
                self.num_donors(),
                self.target(),
                self.nbooks,
                self.nlic,
                self.total_donations(),
                self.status,
                self.org.title,
                self.org.info.email,
                self.org.info.contact_number,
                self.org.info.person1_email,
                self.org.info.person1_phone,
                self.languages]

    def donor_list(self):
        return map(lambda x: x.user_id, self.donations)

    def get_comments(self):
        retval = map(lambda x:x.verbose_fields(),self.comments)
        return retval

    def num_donors(self):
        retval =[]
        for donation in self.donations:
	    if (donation.confirmation):
                retval.append(donation.user_id)
        return len(sets.Set(retval))

    def is_active(self):
        return ((int (self.days_remaining())) > 0 )

    def percent_funded(self):
        return int(round((self.total_donations() * 100) /self.target()))

    def books_donated(self):
        return int(round(self.total_donations() / self.cost_per_book()))

    def needs(self):
        needs = self.target() - self.total_donations() 
        needs = needs if needs > 0 else 0
        return needs


