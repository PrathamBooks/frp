# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from coaster.sqlalchemy import (TimestampMixin,
                                BaseMixin,
                                BaseScopedNameMixin,
                                IdMixin)
# Imported from here by other models

db = SQLAlchemy()

from .user import *
from .org import *
