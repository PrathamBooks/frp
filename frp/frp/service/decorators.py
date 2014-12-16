# -*- coding: utf-8 -*-

"""All decorators required for the project.
"""
from functools import wraps
from flask import session, url_for, redirect, g

from ..models import User


def login_required(f):
    """Decorator to ensure login for given view.
    """
    @wraps(f)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            g.user = User.query.filter_by(email=session.get('email')).first()
            return f(*args, **kwargs)
        return redirect(url_for('login'))
    return inner


def login_required_admin(f):
    """Decorator to ensure login for given view.
    """
    @wraps(f)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            g.user = User.query.filter_by(email=session.get('email')).first()
            if not g.user.is_staff:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return redirect(url_for('login'))
    return inner
