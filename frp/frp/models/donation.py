# -*- coding: utf-8 -*-

import inspect
from datetime import date

from . import db, BaseNameMixin, BaseMixin

__all__ = ['Donation']

class Donation(BaseMixin, db.Model):
    __tablename__ = 'donation'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    confirmation = db.Column(db.Unicode(100), nullable=False)

