# -*- coding: utf-8 -*-

import inspect
from datetime import date

from . import db, BaseNameMixin, BaseMixin

__all__ = ['Comment']

class Comment(BaseMixin, db.Model):
    __tablename__ = 'comment'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    comment = db.Column(db.Unicode(500), nullable=False)


    def get_comment(self):
        return { "date": self.start_date(),
                "by" : self.comment_by.first_name,
                "comment": self.comment}

    def start_date(self):
        return "{:%B %d, %Y}".format(self.created_at.date())

