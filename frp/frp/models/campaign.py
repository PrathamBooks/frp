# -*- coding: utf-8 -*-

from . import db, BaseMixin


class Campaign(BaseMixin, db.Model):
    __tablename__ = 'campaign'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data = db.Column(db.Text(), nullable=False)
