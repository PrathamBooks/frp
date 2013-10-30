from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.lastuser.sqlalchemy import UserBase
from flask.ext.gravatar import Gravatar

from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table




from . import app

db = SQLAlchemy(app)
gravatar = Gravatar()

category_campaign_table = Table('category_campaign', db.metadata,
                                db.Column('category', db.Integer, db.ForeignKey('category.id')),
                                db.Column('campaign', db.Integer, db.ForeignKey('campaign.id'))
)
                                          
class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)


# --- Models ------------------------------------------------------------------

class User(UserBase, db.Model, BaseMixin):
    __tablename__ = 'user'
    description = db.Column(db.Text, default=u'', nullable=False)

    def gravatar(self, **kargs):
        if self.email:
            return gravatar(self.email, **kargs)
        else:
            return ""

    def __repr__(self):
        return "%s"%self.username


class Campaign(db.Model, BaseMixin):
    __tablename__ = "campaign"
    id   = db.Column(db.Integer, primary_key = True)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    approver_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    verifier_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    name = db.Column(db.Text, nullable = False)
    subheading = db.Column(db.Text)
    brief = db.Column(db.Text)
    description = db.Column(db.Text, nullable = False)
    # TBD lat_LNG
    # TBD gallery
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    pledged = db.Column(psql.NUMERIC(precision = 200, scale = 2, asdecimal = True))
    target =  db.Column(psql.NUMERIC(precision = 200, scale = 2, asdecimal = True))
    # TBD email
    # TBD twitter
    # TBD authservice
    created_by = relationship("User", backref = backref('campaigns_created', order_by = id),
                              foreign_keys = [creator_id])
    approved_by = relationship("User", backref = backref('campaigns_approved', order_by = id),
                               foreign_keys = [approver_id])
    approved_on = db.Column(db.DateTime)
    verified_by = relationship("User", backref = backref('campaigns_verified', order_by = id),
                               foreign_keys = [verifier_id])
    verified_on = db.Column(db.DateTime)

    def __repr__(self):
        return "%s"%self.name
    

class Category(db.Model, BaseMixin):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable = False)
    
    icon = db.Column(db.Text)

    campaigns = relationship("Campaign", secondary = category_campaign_table, backref = "categories")

    def __repr__(self):
        return "%s"%self.name
    

class Image(db.Model, BaseMixin):
    __tablename__ = "image"
    id = db.Column(db.Integer, primary_key=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))

    heading = db.Column(db.Text)
    description = db.Column(db.Text)
    url = db.Column(db.Text)
    alt = db.Column(db.Text)
    verified = db.Column(db.Boolean)

    uploaded_by = relationship("User", backref = backref('images', order_by = id))
    campaign = relationship("Campaign", backref = backref('gallery', order_by = id))


    def __repr__(self):
        return "%s"%self.heading




    
    

