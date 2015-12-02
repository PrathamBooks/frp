# -*- coding: utf-8 -*-

import inspect
from datetime import date
from flask import current_app

from . import db, BaseNameMixin, BaseMixin

__all__ = ['Receipt']

class Receipt(BaseMixin, db.Model):
    __tablename__ = 'receipt'
    donation_id = db.Column(db.Integer, db.ForeignKey('donation.id'), nullable=False)
    serial_num = db.Column(db.Integer, nullable=False)
    serial_string = db.Column(db.Unicode(20), nullable=False)
    mail_date = db.Column(db.DateTime, nullable=True)

