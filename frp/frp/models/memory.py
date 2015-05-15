# -*- coding: utf-8 -*-

import inspect
from datetime import date

from . import db, BaseNameMixin, BaseMixin

__all__ = ['Memory']

class Memory(BaseMixin, db.Model):
    __tablename__ = 'memory'
    name = db.Column(db.Unicode(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    city = db.Column(db.Unicode(100), nullable=False)
    state = db.Column(db.Unicode(100), nullable=False)
    email = db.Column(db.Unicode(500), nullable=False)
    can_share = db.Column(db.BOOLEAN, nullable=False)
    words = db.Column(db.Unicode(500), nullable=False)

    def verbose_fields(self):
        return {"date": self.date(),
                "by" : self.name,
                "comment": self.comment}

    def date(self):
        return "{:%B %d, %Y}".format(self.created_at.date())

