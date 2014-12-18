# -*- coding: utf-8 -*-

from . import db, BaseMixin, IdMixin


class Campaign(BaseMixin, IdMixin, db.Model):
    __tablename__ = 'campaign'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data = db.Column(db.Text(), nullable=False)
