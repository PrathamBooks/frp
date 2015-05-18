# -*- coding: utf-8 -*-

import inspect
from datetime import date

from . import db, BaseNameMixin, BaseMixin

__all__ = ['Donation']

COST_PER_BOOK = 50

class Donation(BaseMixin, db.Model):
    __tablename__ = 'donation'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    first_name = db.Column(db.String(50), nullable=False, server_default='')
    last_name = db.Column(db.String(50), nullable=True, server_default='')
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    confirmation = db.Column(db.Unicode(100), nullable=True)
    state = db.Column(db.Unicode(100), nullable=False)
    city = db.Column(db.Unicode(100), nullable=False)
    identification = db.Column(db.Unicode(100), nullable=False)
    identification_type = db.Column(db.Unicode(10), nullable=False)
    ann_choice = db.Column(db.BOOLEAN,nullable=False)
    tax_exemption_certificate = db.Column(db.BOOLEAN,nullable=False)

    def __add__(self,o):
        return self.amount + o.amount
    def __radd__(self,o):
        return self.amount+o

    def donor_name(self):
        if (self.ann_choice == True or (self.donor.first_name == '' and self.donor.last_name == '')):
            return "an Anonymous Donor"
        return self.donor.first_name + ' ' + self.donor.last_name 

    @staticmethod
    def total_donated():
        donations = map(lambda x: x.amount, Donation.query.all())
        return reduce(lambda x, y: x + y, donations)

    @staticmethod
    def total_books_donated():
        return int(round(Donation.total_donated() / COST_PER_BOOK))


    def donation_details(self):
        return [self.first_name +' '+ self.last_name, 
                self.donor.email, 
                self.created_at.date(),
                self.campaign.title,
                self.amount,
                self.ann_choice,
                self.tax_exemption_certificate,
                self.confirmation]

