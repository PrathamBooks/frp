# -*- coding: utf-8 -*-

import inspect
from datetime import date
from flask import current_app

from . import db, BaseNameMixin, BaseMixin

__all__ = ['Donation']

class Donation(BaseMixin, db.Model):
    __tablename__ = 'donation'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    first_name = db.Column(db.String(50), nullable=False, server_default='')
    last_name = db.Column(db.String(50), nullable=True, server_default='')
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    confirmation = db.Column(db.Unicode(100), nullable=True)
    address = db.Column(db.Unicode(500), nullable=False)
    state = db.Column(db.Unicode(100), nullable=False)
    city = db.Column(db.Unicode(100), nullable=False)
    identification = db.Column(db.Unicode(100), nullable=False)
    identification_type = db.Column(db.Unicode(10), nullable=False)
    ann_choice = db.Column(db.BOOLEAN,nullable=False)
    tax_exemption_certificate = db.Column(db.BOOLEAN,nullable=False)
    receipt = db.relationship("Receipt", backref=db.backref("donation"))

    def __add__(self,o):
        return self.amount + o.amount
    def __radd__(self,o):
        return self.amount+o

    def donor_name(self):
        if (self.ann_choice == True):
            return "an Anonymous Donor"
        return self.donor.profile_name()

    @staticmethod
    def total_donated():
        donations = map(lambda x: x.amount, Donation.query.filter(Donation.confirmation != None).all())
        return reduce(lambda x, y: x + y, donations, 0)

    @staticmethod
    def donations_by_date():
        all_donations = Donation.query.filter(Donation.confirmation != None).order_by(Donation.created_at).all()
        return map(lambda x : {"year" : x.created_at.date().year,
                               "month" : x.created_at.date().month,
                               "day" : x.created_at.date().day,
                               "amount" : x.amount,
                               "donor" : x.donor.id
                               }, 
                               all_donations)

    def donation_details(self):
        return [self.first_name +' '+ self.last_name, 
                self.city,
                self.state,
                self.address,
                self.identification_type,
                self.identification,
                self.donor.email, 
                self.created_at.date(),
                self.campaign.title,
                self.amount,
                self.ann_choice,
                self.tax_exemption_certificate,
                self.confirmation]

