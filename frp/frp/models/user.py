# -*- coding: utf-8 -*-

import bcrypt
import coaster

from werkzeug import check_password_hash
from sqlalchemy.orm import defer
from sqlalchemy.ext.hybrid import hybrid_property

from . import db, TimestampMixin, BaseMixin, IdMixin


__all__ = ['User', 'UserInfo', 'USER_STATUS', 'is_username_exists',
           'is_email_exists']


def is_username_exists(username):
    """Check the username exists in db.

    :param username `unicode`: username to check in db.
    """
    return User.query.filter(db.or_(
        User.username == username,
        User.userid == username)).first()


def is_email_exists(email):
    """Check the email exists in db.

    :param username `unicode`: username to check in db.
    """
    return User.query.filter_by(email=email).first()


class USER_STATUS:
    ACTIVE = 0     # Regular, active user
    SUSPENDED = 1  # Suspended account
    INVITED = 2    # Invited to make an account, doesn't have one yet


class User(BaseMixin, db.Model):
    __tablename__ = 'user'
    userid = db.Column(
        db.String(22), unique=True, nullable=False, default=coaster.newid)
    email = db.Column('email', db.Unicode(254), unique=True, nullable=False)
    _username = db.Column(
        'username', db.Unicode(80), unique=True, nullable=True)
    pw_hash = db.Column(db.String(80), nullable=True)
    status = db.Column(
        db.SmallInteger, nullable=False, default=USER_STATUS.ACTIVE)

    # One-one relationship
    userinfo = db.relationship("UserInfo", backref=db.backref("user"),
                               uselist=False)
    organization_created = db.relationship("Organization",
                                           backref=db.backref("created_by"),
                                           uselist=False)


    # Don't load these columns by default
    _defercols = [
        defer('created_at'),
        defer('updated_at'),
        defer('pw_hash'),
        ]

    def __init__(self, password=None, **kwargs):
        self.userid = coaster.newid()
        self.password = password
        super(User, self).__init__(**kwargs)

    @property
    def is_active(self):
        return self.status == USER_STATUS.ACTIVE

    def _set_password(self, password):
        if password is None:
            self.pw_hash = None
        else:
            self.pw_hash = bcrypt.hashpw(
                password.encode('utf-8') if isinstance(password, unicode) else password,
                bcrypt.gensalt())

    #: Write-only property (passwords cannot be read back in plain text)
    password = property(fset=_set_password)

    #: Username (may be null)
    @hybrid_property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not value:
            self._username = None
        elif self.is_valid_username(value):
            self._username = value

    def is_valid_username(self, value):
        if not coaster.valid_username(value):
            return False
        existing = User.query.filter(db.or_(
            User.username == value,
            User.userid == value)).first()  # Avoid User.get to skip status check
        if existing and existing.id != self.id:
            return False

        return True

    def password_is(self, password):
        if self.pw_hash is None:
            return False
        if self.pw_hash.startswith('sha1$'):
            return check_password_hash(self.pw_hash, password)
        else:
            if isinstance(password, unicode):
                password = password.encode('utf-8')
            return bcrypt.hashpw(password, self.pw_hash.encode('utf-8')) == self.pw_hash

    def __repr__(self):
        return u'<User {}>'.format(self.email)


class UserInfo(IdMixin, TimestampMixin, db.Model):
    __tablename__ = 'userinfo'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    first_name = db.Column(db.String(160), nullable=False)
    last_name = db.Column(db.String(160), nullable=True, default=u'')
    address = db.Column(db.String(500), nullable=True, default=u'')
    contact_number = db.Column(db.String(15), nullable=True, default=u'')
    pan_number = db.Column(db.String(10), nullable=True, default=u'')
    need_80g_certificate = db.Column(db.Boolean, default=False,)
