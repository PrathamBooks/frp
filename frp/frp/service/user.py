# -*- coding: utf-8 -*-

from flask import session

from ..models import User


def is_valid_login(email, password):
    """If the username and password hash is matched `g.user` is set else
    False is returned.

    :param email `str`: Email id of the user.
    :param password `str`: Password of the user.
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        return False

    if user.password_is(password):
        session['logged_in'] = True
        session['email'] = user.email
        return True

    return False
