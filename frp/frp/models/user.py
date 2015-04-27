# -*- coding: utf-8 -*-

import bcrypt
import coaster

from werkzeug import check_password_hash
from sqlalchemy.orm import defer
from sqlalchemy.ext.hybrid import hybrid_property
from flask_user import UserMixin

from . import db, TimestampMixin, BaseMixin, IdMixin


__all__ = ['User', 'UserAuth', 'Role', 'USER_STATUS', 
           'is_email_exists', 'admin_user']


def is_email_exists(email):
    """Check the email exists in db.

    :param username `unicode`: username to check in db.
    """
    return User.query.filter_by(email=email).first()

def admin_user():
    return User.query.filter_by(email='infodigital@prathambooks.org').first()

class USER_STATUS:
    ACTIVE = 0     # Regular, active user
    SUSPENDED = 1  # Suspended account
    INVITED = 2    # Invited to make an account, doesn't have one yet


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column('email', db.Unicode(255), unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime())

    # User information
    active = db.Column('enabled', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(50), nullable=False, server_default='')
    last_name = db.Column(db.String(50), nullable=False, server_default='')
    status = db.Column(
        db.SmallInteger, nullable=False, default=USER_STATUS.ACTIVE)
    address = db.Column(db.String(500), nullable=True, default=u'')
    city = db.Column(db.String(100), nullable=True, default=u'')
    state = db.Column(db.String(100), nullable=True, default=u'')
    pin = db.Column(db.String(100), nullable=True, default=u'')
    contact_number = db.Column(db.String(15), nullable=True, default=u'')
    pan_number = db.Column(db.String(10), nullable=True, default=u'')
    need_80g_certificate = db.Column(db.Boolean, default=False,)

    # Relationships
    user_auth = db.relationship('UserAuth', uselist=False)
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))

    organization_created = db.relationship("Organization",
                                           backref=db.backref("created_by"))
    campaigns = db.relationship("Campaign",
                                backref=db.backref("created_by"))
    donations = db.relationship("Donation", backref=db.backref("donor"))
    comments = db.relationship("Comment", backref=db.backref("comment_by"))

    # Don't load these columns by default
    _defercols = [
        defer('created_at'),
        defer('updated_at'),
        defer('pw_hash'),
        ]

    def __repr__(self):
        return u'<User {}>'.format(self.email)

    def profile_name(self):
      if (self.first_name or self.last_name):
        return (self.first_name + ' ' + self.last_name)
      else:
        pos_of_at = self.email.find('@')
        return self.email.substr[:pos_of_at]

# Define the UserAuth data model.
class UserAuth(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))

    # User authentication information (required for Flask-User)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # Relationships
    user = db.relationship('User', uselist=False)


# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))


# Define the UserRoles association model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

