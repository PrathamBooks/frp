from flask import url_for

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.lastuser.sqlalchemy import UserBase
from flask.ext.gravatar import Gravatar

from sqlalchemy.types import UserDefinedType
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table, func, Index, DDL, event




from . import app

db = SQLAlchemy(app)
gravatar = Gravatar()

category_campaign_table = Table('category_campaign', db.metadata,
                                db.Column('category', db.Integer, db.ForeignKey('category.id')),
                                db.Column('campaign', db.Integer, db.ForeignKey('campaign.id'))
)

# --- Custom types ------------------------------------------------------------------
class TsVector(UserDefinedType):
    "Holds a TsVector column"

    name = "TSVECTOR"

    class comparator_factory(UserDefinedType.Comparator):
        """Defines custom types for tsvectors.

        Specifically, the ability to search for ts_query strings using
        the @@ operator.

        On the Python side, this is implemented simply as a `==` operation.

        So, you can do
          Table.tsvector_column == "string"
        to get the same effect as
          tsvector_column @@ to_tsquery('string')
        in SQL

        """

        def __eq__(self, other):
            return self.op('@@')(func.to_tsquery(other))


    def get_col_spec(self):
        return self.name


class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)


# --- Models ------------------------------------------------------------------
# The verbose_fields attribute specifies which attributes to return when a search
# query is done with expand = true


class User(UserBase, db.Model, BaseMixin):
    __tablename__ = 'users'

    description = db.Column(db.Text, default=u'', nullable=False)
    full_text = db.Column(TsVector)

    __table_args__ = (Index('user_full_text_idx', 'full_text', postgresql_using = 'gin'),)

    def gravatar(self, **kargs):
        if self.email:
            return gravatar(self.email, **kargs)
        else:
            return ""

    def verbose_fields(self):
        """Returns data that will be returned to client when this item
        matches a search with expand = True"""
        return dict(username = self.username,
                    fullname = self.fullname,
                    email = self.email,
                    description = self.description)

    def __repr__(self):
        return "%s"%self.username

user_trigger_snippet = DDL("""
CREATE TRIGGER full_text_update BEFORE INSERT OR UPDATE
ON users
FOR EACH ROW EXECUTE PROCEDURE
tsvector_update_trigger(full_text,'pg_catalog.english', 'description')
""")

event.listen(User.__table__, 'after_create', user_trigger_snippet.execute_if(dialect = 'postgresql'))



class Campaign(db.Model, BaseMixin):
    __tablename__ = "campaign"
    id   = db.Column(db.Integer, primary_key = True)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    approver_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    verifier_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    name = db.Column(db.Text, nullable = False)
    subheading = db.Column(db.Text)
    brief = db.Column(db.Text)
    description = db.Column(db.Text, nullable = False)
    latitude = db.Column(psql.NUMERIC(precision = 4, scale = 2, asdecimal = True), nullable = False)
    latitude_hem = db.Column(db.VARCHAR(1), nullable = False)
    longitude = db.Column(psql.NUMERIC(precision = 4, scale = 2, asdecimal = True), nullable = False)
    longitude_hem = db.Column(db.VARCHAR(1), nullable = False)
    # TBD gallery
    start = db.Column(db.DateTime, nullable = False)
    end = db.Column(db.DateTime, nullable = False)
    pledged = db.Column(psql.NUMERIC(precision = 200, scale = 2, asdecimal = True))
    target =  db.Column(psql.NUMERIC(precision = 200, scale = 2, asdecimal = True))
    # email (from created_by)
    # twitter (from created_by)
    # TBD authservice
    created_by = relationship("User", backref = backref('campaigns_created', order_by = id),
                              foreign_keys = [creator_id])
    approved_by = relationship("User", backref = backref('campaigns_approved', order_by = id),
                               foreign_keys = [approver_id])
    approved_on = db.Column(db.DateTime)
    verified_by = relationship("User", backref = backref('campaigns_verified', order_by = id),
                               foreign_keys = [verifier_id])
    verified_on = db.Column(db.DateTime)
    full_text = db.Column(TsVector)

    __table_args__ = (Index('campaign_full_text_idx', 'full_text', postgresql_using = 'gin'),)




    def __repr__(self):
        return "%s"%self.name

campaign_trigger_snippet = DDL("""
CREATE TRIGGER full_text_update BEFORE INSERT OR UPDATE
ON campaign
FOR EACH ROW EXECUTE PROCEDURE
tsvector_update_trigger(full_text,'pg_catalog.english', 'name', 'subheading', 'brief', 'description')
""")

event.listen(Campaign.__table__, 'after_create', campaign_trigger_snippet.execute_if(dialect = 'postgresql'))



class Category(db.Model, BaseMixin):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable = False)

    icon = db.Column(db.Text)

    campaigns = relationship("Campaign", secondary = category_campaign_table, backref = "categories")


    @property
    def icon_url(self):
        if self.icon:
            return "/category/%s/icon"%(self.id)
        else:
            return url_for('static', filename='images/unspecified.png')

    def __repr__(self):
        return "%s"%self.name


class Image(db.Model, BaseMixin):
    __tablename__ = "image"
    id = db.Column(db.Integer, primary_key=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"))
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
